from datetime import datetime, timedelta
import json
from threading import Lock
import time
from django import template
from django.db import models
#import Levenshtein
from django.http import JsonResponse
#from fuzzywuzzy import fuzz
from django.db.models import Q
import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

# 工具类文件，存放其他接口
weather_cache = {}
cache_lock = Lock()
CACHE_DURATION = timedelta(minutes=5)  # 缓存时间设置为5分钟

register = template.Library()


@register.filter  # 弃用
def truncate_string(value, max_length):
    if len(value) > max_length:
        return value[:max_length]
    else:
        return value


@register.filter   #弃用
def reverse_truncate_string(value, max_length):
    if len(value) > max_length:
        return value[-max_length:]
    else:
        return value


register.filter("truncatestring", truncate_string)
register.filter("reverse_truncatestring", reverse_truncate_string)


class Res_Manager(models.Manager):
    """ def res_filter(self, istr):
        query = self.all().order_by("res_time")
        for i in query:
            user = str(i.user.username)
            if (
                Levenshtein.distance(user, istr) <= len(user) / 3  # 莱文斯坦距离
                or fuzz.partial_ratio(user, istr) >= 60  # 模糊匹配
                or str(istr).lower() in user.lower()  # 包含
            ):
                continue
            else:
                query = query.exclude(title=i.title)
        return query """

    def filter_reservations(self, search_value):
        # 进行模糊查询，针对多个字段
        return self.filter(
            Q(description__icontains=search_value)
            | Q(device__name__icontains=search_value)
            | Q(inviter__username__icontains=search_value)
            | Q(res_user__username__icontains=search_value)
            | Q(res_time__icontains=search_value)
            | Q(audit_time__icontains=search_value)
        )


def get_true_verbose_names(instance, target_fields):  # 针对时段管理获取可用小时
    true_verbose_names = []

    for field_name in target_fields:
        # 使用模型实例的 _meta 方法获取该字段
        field = instance._meta.get_field(field_name)
        field_value = getattr(instance, field_name, None)
        if field_value:  # 如果该字段的值为 True
            true_verbose_names.append(field.verbose_name)

    return true_verbose_names


@csrf_exempt
def get_weather(request):
    city = request.POST.get("city")
    key = "d2ef7258c237ba8683e377cbb02770cf"
    geo_api = f"http://api.openweathermap.org/geo/1.0/direct?q={city},cn&appid={key}&lang=zh_cn"

    if request.method == "POST":
        with cache_lock:
            # 检查缓存是否存在且未过期
            if city in weather_cache:
                cached_data, timestamp = weather_cache[city]
                if datetime.now() - timestamp < CACHE_DURATION:
                    return JsonResponse(cached_data)

        try:
            # 获取地理信息
            geo = json.loads(requests.get(geo_api, verify=False).text)
            lat = geo[0]["lat"]
            lon = geo[0]["lon"]
            data_api = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}&lang=zh_cn"
            data_temp = requests.get(data_api, verify=False)
            data = json.loads(data_temp.text)

            # 处理天气数据
            temp = round((float(data["main"]["temp"]) - 273.15), 2)
            feels_temp = round((float(data["main"]["feels_like"]) - 273.15), 2)
            pressure = data["main"]["pressure"]
            humi = data["main"]["humidity"]
            wind = data["wind"]
            weather = data["weather"][0]["main"]
            description = data["weather"][0]["description"]
            icon = data["weather"][0]["icon"]
            clouds = data["clouds"]["all"]
            sunrise_temp = data["sys"]["sunrise"]
            sunset_temp = data["sys"]["sunset"]
            sunrise = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(sunrise_temp))[
                -8:
            ]
            sunset = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(sunset_temp))[
                -8:
            ]

            # 构建返回数据
            weather_data = {
                "temp": temp,
                "feels_temp": feels_temp,
                "pressure": pressure,
                "humi": humi,
                "wind": wind,
                "weather": weather,
                "description": description,
                "icon": icon,
                "clouds": clouds,
                "sunrise": sunrise,
                "sunset": sunset,
            }

            # 更新缓存
            weather_cache[city] = (weather_data, datetime.now())

            return JsonResponse(weather_data)

        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return JsonResponse({"error": "无法获取天气数据"}, status=500)

    return JsonResponse({"error": "无效的请求"}, status=400)

