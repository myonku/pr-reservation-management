#注意：此文件中的接口方法是为模板文件设计，大部分已经弃用，但保留以供参考


import datetime
import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
import urllib3
from resvation.models import time_sep, user
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from api.serializers import *
from django.db.models import Q
import requests, json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from rest_framework.response import Response

# Create your views here.,

urllib3.disable_warnings()


def error_page(request):
    return render(request, "error.html")


def get_error_data(request, error=None, info=None):
    code = int(request.POST.get("code"))
    li = [
        {"error": 400, "info": "错误请求!请检查您的请求是否正确"},   #1
        {"error": 401, "info": "您未通过身份验证，请重新登录或刷新页面"},
        {"error": 403, "info": "服务器拒绝了请求"},                #3
        {"error": 404, "info": "服务器找不到请求的网页"},
        {"error": 408, "info": "服务器等候请求时超时"},             #5
        {"error": 499, "info": "服务端处理时间过长，客户端已关闭连接"},
        {
            "error": 503,
            "info": "目前无法使用服务器（由于超载或进行停机维护）。通常，这只是一种暂时的状态",  #7
        },
    ]

    context = li[code - 1]
    return JsonResponse(context)


# 用户认证部分
@csrf_exempt
@api_view(["POST"])
def username_validator(request):

    name = request.POST.get("username")
    if user.objects.filter(username=name).exists():
        return JsonResponse(
            {"result":False}
        )
    else:
        return JsonResponse(
            {"result":True}
        )


def login_Action(request):
    if request.user.is_authenticated:
        name = request.user.username
        logout(request)
        messages.success(request, "当前用户 " + name + " 已注销。")
        return render(request, "auth/login.html")
    else:
        return render(request, "auth/login.html")


def logins(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        iuser = authenticate(request, username=username, password=password)
        if iuser is not None:
            login(request, iuser)
            messages.success(request, message="欢迎，" + iuser.username + "!")
            if iuser.if_staff == 1:
                return redirect("/admins")    #直接跳转到管理后台（测试用）
            else:
                return redirect("/loginAction")
        else:
            messages.error(request, "用户名或密码错误！")
            return redirect("/loginAction")
    else:
        return Response({"error": ""})


def register(request):
    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if email == "":
            email = None
        else:
            iuser = user.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=0,
                if_staff=0,
                is_active=1,
                is_superuser=0,
            )
            iuser.save()
        messages.success(request, "已成功注册，即将前往登录")
        return redirect("/loginAction")
    else:
        return Response({"error": ""})


def adminin(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return HttpResponseRedirect("/admins")
        else:
            messages.error(request, "当前用户无后台权限！")
            return None
    else:
        return Response({"error": ""})


# 天气数据接口：openweather api
@csrf_exempt
def get_weather(request):

    city = request.POST.get("city")     
    key = "d2ef7258c237ba8683e377cbb02770cf"
    geo_api = f"http://api.openweathermap.org/geo/1.0/direct?q={city},cn&appid={key}&lang=zh_cn"
    if request.method == "POST":
        try:
            geo = json.loads(requests.get(geo_api, verify=False).text)
            lat = geo[0]["lat"]
            lon = geo[0]["lon"]
            data_api = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}&lang=zh_cn"
            data_temp = requests.get(data_api, verify=False)
            data = json.loads(data_temp.text)
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
            sunrise = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(sunrise_temp))[-8:]
            sunset = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(sunset_temp))[-8:]
            data = {
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
        except:
            data = {}
        return JsonResponse(data)

    else:
        return Response({"error": ""})


# index路由部分（数据总览部分）

@csrf_exempt
def get_Charts(request):
    if request.method == "POST" or request.method == "OPTIONS":
        day1 = int(request.POST.get("day1"))
        day2 = int(request.POST.get("day2"))
        day3 = int(request.POST.get("day3"))
        date0 = datetime.datetime.now()
        # 测试：该部分数据为距今x天之前的部分

        def recent_res(day=7):  # day1 时段内的预约数量分布
            count = []
            for i in range(day):
                date = date0 - datetime.timedelta(days=i)
                temp = origin_resvation.objects.filter(
                    Q(res_start_time__year=date.year)
                    & Q(res_start_time__month=date.month)
                    & Q(res_start_time__day=date.day)
                ).count()
                count.append(temp)
            count.reverse()
            return count

        def period_res(day=14):  # 时间段分布，数据暂定为为x天前开始的部分
            date = datetime.datetime.now() - datetime.timedelta(days=day)
            total = origin_resvation.objects.filter(res_start_time__gte=date)
            count = []
            for i in range(8):
                time = datetime.datetime.now().replace(
                    hour=0, minute=0, second=0
                ) + datetime.timedelta(hours=(i + 1) * 3)
                time_e = time - datetime.timedelta(hours=3)
                temp = total.filter(
                    Q(res_start_time__hour__gt=time_e.hour)
                    & Q(res_start_time__hour__lt=time.hour)
                ).count()
                count.append(temp)
            return count

        def device_sep(day=30):  # 通道分布
            list0 = device.objects.annotate(
                res_count=Count(
                    "res_device",
                    filter=Q(
                        res_device__res_start_time__gte=date0 - datetime.timedelta(days=day)
                    ),
                )
            )
            names = [i.name for i in list0]
            count = [i.res_count for i in list0]

            return {
                "count": count,
                "names": names,
            }

        context = {
            "data1": recent_res(day1),
            "data2": period_res(day2),
            "data3": device_sep(day3),
        }
        return JsonResponse(context)
    else:
        return Response({"error": ""})


def index(request):
    if request.user.is_authenticated:
        get_Charts(request)
        return render(request, "home/index.html")
    else:
        return render(request, "func/rserve.html")


def registerAction(request):
    return render(request, "auth/register.html")


def reserve_sub(request):
    pass

def reprovice(request):
    pass


# verif路由（预约申请管理部分）

@csrf_exempt
def get_res_list(request):
    if request.method == "POST":
        key = request.POST.get("key")
        if key == "1":
            query = (
                origin_resvation.objects.exclude(state="2")
                .exclude(state="3")
                .filter(
                    Q(res_time__gte=datetime.datetime.now() - datetime.timedelta(days=15))
                )
                .order_by("res_time")               # 15天内待审核的记录
            )
        elif key == "0":
            query = origin_resvation.objects.all().order_by("res_time")
        elif key == "2":
            iuser = request.user
            query = iuser.res_user.all()

        queryset = ResvationSerializer(query, many=True).data            #序列化
        if queryset != None:
            paginator = Paginator(queryset, 15)  # 实例化分页对象
            page = request.POST.get("page_num")  # 从URL通过get页码
            try:
                page_obj = paginator.page(page)
            except PageNotAnInteger:
                page_obj = paginator.page(1)  # 如果传入page参数不是整数，默认第一页
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            is_paginated = (
                True if paginator.num_pages > 1 else False
            )  # 如果页数小于1不使用分页
            page_last = paginator.num_pages
            start = (int(request.POST.get("page_num", 1)) - 1) * 15
            context = {
                "page": list(page_obj),
                "is_paginated": is_paginated,
                "page_last": page_last,
                "current_start": start,
                "if_has_previous": page_obj.has_previous(),
                "if_has_next": page_obj.has_next(),
                "pagenum": page_obj.number,
            }
            return JsonResponse(context)
        else:
            context = {
                "page": "",
            }
            return JsonResponse(context)
    else:
        return Response({"error": ""})


@csrf_exempt
@api_view(["POST"])
def get_apd_report(request):
    iuser = request.user
    if iuser.is_authenticated:
        if iuser.if_staff:
            query = approved_reservation.objects.all().order_by("-id")
        else:
            query = approved_reservation.objects.filter(origin_resvation__res_user=iuser).order_by("-id")

        queryset = APD_ResvationSerializer(query, many=True).data

        if queryset != None:
            paginator = Paginator(queryset, 12)
            page = request.POST.get("page_num")
            try:
                page_obj = paginator.page(page)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            is_paginated = (
                True if paginator.num_pages > 1 else False
            )
            page_last = paginator.num_pages
            start = (int(request.POST.get("page_num", 1)) - 1) * 12
            context = {
                "page": list(page_obj),
                "is_paginated": is_paginated,
                "page_last": page_last,
                "current_start": start,
                "if_has_previous": page_obj.has_previous(),
                "if_has_next": page_obj.has_next(),
                "pagenum": page_obj.number,
            }
            return JsonResponse(context)
        else:
            context = {
                "page": "",
            }
            return JsonResponse(context)
    else:
        return redirect("/error/?message=2")


def get_res_detail(request):
    if request.method == "POST":
        res_id = request.POST.get("res_id")
        resvation = origin_resvation.objects.filter(id = res_id)
        iuser = resvation.res_user
        devi = resvation.device
        res_user = S_UserSerializer(iuser, many=False)
        res_detail = ResvationSerializer(resvation, many=False)
        res_device = DeviceSerializer(devi, many=False)
        return JsonResponse({
            "res_detail" : res_detail,
            "res_user" : res_user,
            "res_device" : res_device,
        })
    else:
        return Response({"error": ""})

def valid_res_list(request):
    get_res_list(request)
    return render(request, "resview/res_list.html")


def all_res_list(request):
    get_res_list(request)
    return render(request, "resview/all_list.html")

def apd_record_list(request):
    get_apd_report(request)
    return render(request, "resview/apd_list.html")


def search_result(request):
    pass


def res_detail(request):
    return render(request, "resview/res_detail.html")


# 管理

def get_sep_data(request):
    if request.method == "POST":
        idate = request.POST.get("date")
        isep = time_sep.objects.filter(date = idate)
        if isep.exists():
            timesep = Time_SepSerializer(isep, many=False)
        else:
            time_sep.objects.create(date = idate)
            esep = time_sep.objects.filter(date=idate)
            timesep = Time_SepSerializer(esep, many=False)
        context = {
            "timesep" : timesep,
        }
        return JsonResponse(context)
    else:
        return Response({"error": ""})


def sep_manage(request):
    return render(request, "elcmanage/sep_manage.html")


def device_manage(request):
    return render(request, "elcmanage/device_manage.html")


# 用户操作

def add_res_rec(request):
    if request.method == "POST":
        format = r"%Y-%m-%d %H:%M:%S"
        name1 = request.POST.get("username")
        iuser = user.objects.filter(username = name1)
        name2 = request.POST.get("inviter")
        iinviter = user.objects.filter(username = name2)
        start = request.POST.get("start")
        device_name = request.POST.get("device")
        idevice = device.objects.filter(name = device_name)
        idescription = request.POST.get("description")
        user.objects.create(
            res_user=iuser,
            inviter=iinviter,
            res_start_time=datetime.datetime.strptime(start, format),
            device=idevice,
            description=idescription
        )
        context = {"data": "提交成功！"}
        return JsonResponse(context)
    else:
        return Response({"error": ""})


def get_self_res(request):    #申请记录
    return get_res_list(request)


def get_apd_res(request):    #通过记录
    get_apd_report(request)
    return render()
