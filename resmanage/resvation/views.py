import datetime
import json
import time

from api.utils import get_true_verbose_names
from resvation.models import time_sep, user, approved_reservation, origin_resvation
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from api.serializers import *
from django.db.models import Q
from django.db.models import Count
from django.contrib.auth.models import update_last_login
# from api.extra_package import manage_frames
from api import face_identity
# Create your views here.


# 用户认证部分
@csrf_exempt
@api_view(["POST"])
def username_validator(request):                   
    """注册时验证用户名合法性"""
    name = request.POST.get("username")
    if user.objects.filter(username=name).exists():
        return JsonResponse({"result": False})
    else:
        return JsonResponse({"result": True})


@csrf_exempt
@api_view(["POST"])
def verify_token(request):
    """验证tokrn（配合vue路由守卫）"""
    token = request.data.get("token") 
    if not token:
        return Response({"error": "Token is required."}, status=status.HTTP_200_OK)
    try:
        # 检查 token 是否存在，并获取该 token 关联的用户
        token_instance = Token.objects.get(key=token)
        user = token_instance.user
        # 这里可以根据需要添加额外的验证，比如检查用户的状态
        if user.is_active:  # 确保用户是活动状态
            if user.if_staff:
                return Response(
                    {"valid": True, "user_id": user.id, "staff": True},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"valid": True, "user_id": user.id, "staff": False},
                    status=status.HTTP_200_OK,
                )
        else:
            return Response({"valid": False}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({"valid": False}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def v_login(request):
    """登录接口"""
    username = request.data.get("username")
    password = request.data.get("password")
    iuser = authenticate(request, username=username, password=password)
    if iuser is not None:
        update_last_login(None, iuser)  # 自动更新 last_login
        iuser.save()                                # 保存更改到数据库
        key_value = 0 if iuser.if_staff else 1
        token, created = Token.objects.get_or_create(user=iuser)
        return Response(
            {"token": token.key, "key": key_value}, status=status.HTTP_200_OK
        )
    else:
        return Response({"token": "", "key": 10}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def v_register(request):
    """注册接口"""
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
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
            common_staff=0,
        )
        iuser.save()
    return Response({"key": 0}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def get_user_info(request):
    """获取基本用户数据"""
    token = request.data.get("token")
    if not token:
        return Response(
            {"error": "Token is required."}, status=status.HTTP_400_BAD_REQUEST
        )
    token_instance = Token.objects.get(key=token)
    user = token_instance.user
    return Response(
        {
            "username": user.username,
            "avatar": user.profile.url,
            "is_staff": user.is_staff,
        },
    )


@csrf_exempt
@api_view(["POST"])
def update_qrcode(request):
    """更新二维码"""
    token = request.data.get("token")
    if not token:
        return Response(
            {"error": "Token is required."}, status=status.HTTP_400_BAD_REQUEST
        )
    token_instance = Token.objects.get(key=token)
    user = token_instance.user
    user.update_qrcode()
    return Response(
        {
            "qr_data": user.qr_data,
        },
    )


@csrf_exempt
@api_view(["POST"])
def get_user_detail(request):
    """获取用户数据（个人信息页面）"""
    token = request.data.get("token")
    if not token:
        return Response(
            {"error": "Token is required."}, status=status.HTTP_400_BAD_REQUEST
        )
    token_instance = Token.objects.get(key=token)
    user = token_instance.user
    return Response(
        {
            "username": user.username,
            "avatar": user.profile.url,
            "if_staff": user.if_staff,
            "phone": user.phone_number,
            "email": user.email,
            "date_joined": user.date_joined.strftime("%Y-%m-%d %H:%M"),
            "last_login": (
                user.last_login.strftime("%Y-%m-%d %H:%M") if user.last_login else None
            ),
            "common_staff": user.common_staff,
            "qr_data": user.qr_data,
            "identity_code": (
                True if user.identity_code and user.identity_code != "" else False
            ),
        }
    )


#
@csrf_exempt
@api_view(["POST"])
def getchart1(request):
    """图表（折线）"""
    day = int(request.data.get("day"))
    dfor = request.data.get("for")
    datex = datetime.datetime.now()
    count = []
    if dfor == "0":
        for i in range(day):
            date = datex - datetime.timedelta(days=i)
            temp = origin_resvation.objects.filter(
                Q(res_time__year=date.year)
                & Q(res_time__month=date.month)
                & Q(res_time__day=date.day)
            ).count()
            count.append(temp)
    else:
        for i in range(day):
            date = datex - datetime.timedelta(days=i)
            temp = origin_resvation.objects.filter(
                Q(res_start_time__year=date.year)
                & Q(res_start_time__month=date.month)
                & Q(res_start_time__day=date.day)
            ).count()
            count.append(temp)
    count.reverse()
    return Response(count)


@csrf_exempt
@api_view(["POST"])
def getchart2(request):
    """图表（柱状）"""
    day = int(request.data.get("day"))
    date = datetime.datetime.now() - datetime.timedelta(days=day)
    total = origin_resvation.objects.filter(res_start_time__gte=date)
    count = []
    for i in range(8):
        time = datetime.datetime.now().replace(
            hour=0, minute=0, second=0
        ) + datetime.timedelta(hours=(i + 1) * 3)
        time_e = time - datetime.timedelta(hours=3)
        temp = total.filter(
            Q(res_start_time__hour__gte=time_e.hour)
            & Q(res_start_time__hour__lt=time.hour)
        ).count()
        count.append(temp)
    return Response(count)


@csrf_exempt
@api_view(["POST"])
def getchart3(request):
    """图表（饼图）"""
    day = int(request.data.get("day"))
    date = datetime.datetime.now() - datetime.timedelta(days=day)
    list0 = device.objects.annotate(
        res_count=Count(
            "res_device",
            filter=Q(
                res_device__res_start_time__gte=date - datetime.timedelta(days=day)
            ),
        )
    )
    names = [i.name for i in list0]
    count = [i.res_count for i in list0]
    return Response(
        {
            "count": count,
            "names": names,
        }
    )


# 数据展示部分


@csrf_exempt
@api_view(["POST"])
def v_res_list(request):
    """待审核记录/全部记录（针对ori_res...模型）（个人/管理员）"""
    key = request.data.get("key")

    sortBy = request.data.get("sortBy")
    isDescending = request.data.get("isDescending")
    if sortBy == "1":
        isort = "res_start_time"
    elif sortBy == "2":
        isort = "res_time"
    elif sortBy == "3":
        isort = "res_end_time"
    else:
        isort = "id"

    if isDescending == "true":  # bool传成字符串了
        sort = f"-{isort}"
    else:
        sort = isort

    if key == "1":
        query = origin_resvation.objects.filter(state="1")
    elif key == "0":
        query = origin_resvation.objects.all()
    elif key == "2":
        token = request.data.get("token")
        if not token:
            return Response({"error": "Token is required."}, status=status.HTTP_200_OK)
        token_instance = Token.objects.get(key=token)
        user = token_instance.user
        query = user.res_user.all()

    query = query.order_by(sort)

    queryset = (
        ResvationSerializer(query, many=True).data
        if key != "2"
        else UTR_ResvationSerializer(query, many=True).data
    )  # 序列化
    if queryset != None:
        per_page = 15 if key != "2" else 10
        paginator = Paginator(queryset, per_page)  # 实例化分页对象
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
        start = (int(request.data.get("page_num", 1)) - 1) * 15
        context = {
            "page": list(page_obj),
            "is_paginated": is_paginated,
            "page_last": page_last,
            "current_start": start,
            "if_has_previous": page_obj.has_previous(),
            "if_has_next": page_obj.has_next(),
            "pagenum": page_obj.number,
            "total": paginator.count,
        }
        return JsonResponse(context)
    else:
        context = {
            "page": "",
        }
        return JsonResponse(context)


@csrf_exempt
@api_view(["POST"])
def v_apd_report(request):
    """已通过申请记录（个人/管理员）"""
    token = request.data.get("token")
    sortBy = request.data.get("sortBy")
    isDescending = request.data.get("isDescending")

    if sortBy == "1":
        isort = "origin_resvation__res_start_time"
    elif sortBy == "2":
        isort = "origin_resvation__audit_time"
    else:
        isort = "id"

    if isDescending == "true":
        sort = f"-{isort}"
    else:
        sort = isort

    if not token:
        return Response(
            {"error": "Token is required."}, status=status.HTTP_400_BAD_REQUEST
        )
    token_instance = Token.objects.get(key=token)
    iuser = token_instance.user

    if iuser.is_authenticated:
        if iuser.if_staff:
            query = approved_reservation.objects.all().order_by(sort)
        else:
            query = approved_reservation.objects.filter(
                origin_resvation__res_user=iuser
            ).order_by(sort)

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
            is_paginated = True if paginator.num_pages > 1 else False
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
                "total": paginator.count,
            }
            return JsonResponse(context)
        else:
            context = {
                "page": "",
            }
            return JsonResponse(context)
    else:
        return Response({"error": ""}, status=status.HTTP_401_UNAUTHORIZED)


@csrf_exempt
@api_view(["POST"])
def get_all_dev(request):
    """获取所有通道"""
    if request.data.get("key") == 1:
        dev = device.objects.all().values_list("name", flat=True)
        return JsonResponse({"list": list(dev)})
    else:
        return Response({"error": ""}, status=status.HTTP_401_UNAUTHORIZED)


@csrf_exempt
@api_view(["POST"])
def get_all_valid_date(request):
    """获取所有可用日期"""
    date = datetime.datetime.today()
    start = date + datetime.timedelta(days=3)
    end = date + datetime.timedelta(days=10)
    if request.data.get("key") == 1:
        k = time_sep.objects.filter(
            date__gte=start.replace(hour=0, minute=0, second=0),
            date__lt=end.replace(hour=0, minute=0, second=0),
            if_valid=True,
        ).values_list("date", flat=True)
        return JsonResponse({"list": list(k)})
    else:
        return Response({"error": ""}, status=status.HTTP_401_UNAUTHORIZED)


@csrf_exempt
@api_view(["POST"])
def get_base_date_info(request):
    """获取基本信息（用户预约）"""
    date = datetime.datetime.today()
    start = date + datetime.timedelta(days=3)
    start = start.replace(hour=0,minute=0,second=0)
    end = date + datetime.timedelta(days=10)
    end = end.replace(hour=0, minute=0, second=0)
    res = time_sep.objects.filter(
        date__gte=start,
        date__lt=end,
    )
    listx = []
    for i in res:
        temp = {
            "date": i.date.strftime("%Y-%m-%d"),
            "valid": i.if_valid,
            "limit": i.get_max_resnum_display(),
            "interval": i.interval
        }
        listx.append(temp)
    return Response(listx, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def get_date_hours(request):
    """获取可预约时刻"""
    temp = request.data.get("date")
    target_fields = [f"hour_{i}" for i in range(24)]  # 所有 24 个小时的字段
    datex = datetime.datetime.strptime(temp, "%Y-%m-%d")
    date = time_sep.objects.get(date=datex)
    interval = date.interval
    true_names = get_true_verbose_names(date, target_fields)
    return Response({'hours': true_names, 'interval': interval})


@csrf_exempt
@api_view(["POST"])
def get_search_result(request):
    """搜索功能"""
    key = request.data.get("input")
    datesc = request.data.get("datesc")
    timesc = request.data.get("timesc")
    dateRange = request.data.get("dateRange")
    timeRange = request.data.get("timeRange")
    cate = request.data.get("cate")
    value = request.data.get("value")
    sortBy = request.data.get("sortBy")
    isDescending = request.data.get("isDescending")

    if not key.isspace():
        if sortBy == "1":
            isort = "res_start_time"
        elif sortBy == "2":
            isort = "res_time"
        else:
            isort = "id"

        sort = f"-{isort}" if isDescending == "true" else isort
        obj = origin_resvation.objects.filter_reservations(key).order_by(sort)
        query = obj.filter(state="2") if cate == "1" else obj

        if dateRange:
            date = str(dateRange).split(",")
            datesatrt = datetime.datetime.strptime(date[0], "%Y-%m-%d").date()
            dateend = datetime.datetime.strptime(date[1], "%Y-%m-%d").date()
            if datesc == "1":
                query = query.filter(
                    Q(res_time__gte=datesatrt) & Q(res_time__lt=dateend)
                )
            else:
                query = query.filter(
                    Q(res_start_time__gte=datesatrt) & Q(res_start_time__lt=dateend)
                )

        if timeRange:
            time = str(timeRange).split(",")
            timestart = datetime.datetime.strptime(time[0], "%H:%M").time()
            timeend = datetime.datetime.strptime(time[1], "%H:%M").time()
            if timesc == "1":
                query = query.filter(
                    Q(res_time_only__gte=timestart) & Q(res_time_only__lt=timeend)
                )
            else:
                query = query.filter(
                    Q(res_start_time_only__gte=timestart)
                    & Q(res_start_time_only__lt=timeend)
                )

        if value:
            vlist = str(value).split(",")
            query = query.filter(device__name__in=vlist)

        queryset = ResvationSerializer(query, many=True).data  # 序列化

        if queryset != None:
            paginator = Paginator(queryset, 10)  # 实例化分页对象
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
            start = (int(request.data.get("page_num", 1)) - 1) * 10
            context = {
                "page": list(page_obj),
                "is_paginated": is_paginated,
                "page_last": page_last,
                "current_start": start,
                "if_has_previous": page_obj.has_previous(),
                "if_has_next": page_obj.has_next(),
                "pagenum": page_obj.number,
                "total": paginator.count,
            }
            return JsonResponse(context)
        else:
            return JsonResponse(
                {
                    "page": "",
                    "is_paginated": 0,
                    "page_last": page_last,
                    "current_start": start,
                    "if_has_previous": 0,
                    "if_has_next": 0,
                    "pagenum": 1,
                    "total": 0,
                }
            )
    else:
        return Response({"error": "not empty string!"})


##管理部分


@csrf_exempt
@api_view(["POST"])
def get_appointments(request):
    """获取时段分配数据"""
    date_str = request.data.get("date")
    if not date_str:
        return Response({"error": "Date is required"}, status=400)
    try:
        # 将字符串转换为日期对象
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)
    cord = time_sep.objects.filter(date=date).first()
    if not cord:
        cord = time_sep.objects.create(date=date)

    data = Time_SepSerializer(cord, many=False).data
    return Response(data)


@csrf_exempt
@api_view(["POST"])
def update_appointments(request):
    """更新时段分配数据"""
    date_str = request.data.get("date")
    isDateUnavailable = request.data.get("isDateUnavailable") == "true"
    maxAppointments = int(request.data.get("maxAppointments"))
    selectedTime = int(request.data.get("selectedTime"))
    selectedHours = request.data.get("selectedHours").split(",")
    start = datetime.datetime.today() + datetime.timedelta(days=3)
    end = datetime.datetime.today() + datetime.timedelta(days=10)
    try:
        # 将字符串转换为日期对象
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)
    if request.data.get("date") == "1999-01-01":
        cords = time_sep.objects.filter(
            date__gte=start.replace(hour=0, minute=0, second=0),
            date__lt=end.replace(hour=0, minute=0, second=0),
        )
    else:
        cords = time_sep.objects.filter(date=date)

    try:
        for cord in cords:
            cord.if_valid = not isDateUnavailable
            if not isDateUnavailable:
                if maxAppointments == 99999998:
                    maxc = 0
                elif maxAppointments == 99999999:
                    maxc = 4
                elif maxAppointments == 10:
                    maxc = 1
                elif maxAppointments == 50:
                    maxc = 2
                elif maxAppointments == 100:
                    maxc = 3
                cord.max_resnum = maxc
                cord.interval = selectedTime

                for hour in range(24):
                    setattr(cord, f"hour_{hour}", selectedHours[hour] == "true")
            cord.transform_num = cord.transform_num + 1
            cord.updated_at = datetime.datetime.now()
            cord.save()
        status = "success"
        message = "数据更新成功！"
    except:
        status = "error"
        message = "服务器错误，数据更新失败！"

    return Response({"status":status, "message":message})


@csrf_exempt
@api_view(["POST"])
def get_date_detail(request):
    """遗漏接口"""
    date_str = request.data.get("date")
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    cord = time_sep.objects.get(date=date)
    return Response(
        {
            "transform_num": cord.transform_num,
            "updated_at": datetime.datetime.strftime(cord.updated_at, "%Y-%m-%d %H:%M"),
        }
    )


@csrf_exempt
@api_view(["POST"])
def get_record_detail(request):
    """获取记录内容"""
    key = int(request.data.get("key"))
    id = int(request.data.get("id"))
    if key == 0:
        result = ResvationSerializer(
            origin_resvation.objects.get(id=id), 
            many=False
            ).data

    elif key == 1:
        result = APD_ResvationSerializer(
            approved_reservation.objects.get(id=id),
            many=False
        ).data
    return Response(result)


@csrf_exempt
@api_view(["POST"])
def asc_record(request):
    """审核（动词）记录"""
    id = int(request.data.get("id"))
    mot = request.data.get("manage")
    token = request.data.get("token")
    if not token:
        return Response({"key": 1, "context": "用户信息校验出错，更新失败！"})
    token_instance = Token.objects.get(key=token)
    iuser = token_instance.user
    state = "2" if mot == "0" else "3"
    try:
        xc = origin_resvation.objects.filter(id = id)
        xc.update(
            audit_staff=iuser,
            audit_time=datetime.datetime.now(),
            msg_phase=3,
            state=state
        )
        ci = 0
        if mot == "0":
            approved_reservation.objects.create(origin_resvation=xc.first())
        context = (
            "操作成功,该条记录已通过！" if mot == "0" else "操作成功,已拒绝该条记录！"
        )
    except:
        ci = 1
        context = "服务器内部错误，操作失败！"
    return Response({
        "key": ci,
        "context": context
    })


# 用户操作


@csrf_exempt
@api_view(["POST"])
def resvation_submit(request):
    """申请提交逻辑"""
    name = request.data.get('name')
    if name:
        iuser = user.objects.get(username=name)
        date = request.data.get("date")
        timestart = request.data.get("timestart")
        timeend = request.data.get("timeend")
        datetime_str = f"{date} {timestart}"
        end_str = f"{date} {timeend}"
        add_inviter = request.data.get("add_inviter")
        inviter = request.data.get("inviter") if add_inviter else None
        in_e = user.objects.get(username = inviter) if inviter else None
        dev = device.objects.get(name=request.data.get("device"))
        desc = request.data.get("desc")
        start = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        end = datetime.datetime.strptime(end_str, "%Y-%m-%d %H:%M").replace(minute=59).replace(second=59)
        temp = time_sep.objects.get(date=start.date())

        max_num = (
            temp.get_max_resnum_display() / 10
            if temp.max_resnum in [1, 2, 3]
            else 99999999
        )

        if origin_resvation.objects.filter(
            res_start_time__year=start.year,
            res_start_time__month=start.month,
            res_start_time__day=start.day,
        ).count() >= max_num:
            return Response(
                {"state": 1, "error": "您在目标日期的申请已达到了最大限制！"}
            )
        else:
            if origin_resvation.objects.filter(
                res_user=iuser,
                res_start_time=start,
            ).exists():
                return Response({"state": 1, "error": "已存在该时间段的申请记录，请勿重复提交！"})
            else:
                try:
                    origin_resvation.objects.create(
                        res_user=iuser,
                        device=dev,
                        description=desc,
                        inviter=in_e,
                        res_start_time=start,
                        res_dec_time=end
                    )
                    return Response({"state": 0, "success": "申请提交成功！"})
                except:
                    return Response({"state": 1, "error": "提交失败，请稍后重试！"})

    else:
        return Response({"state": 1, "error": "数据错误，无法验证用户名！"})

"""
# 将 JSON 字符串转换为 Python 列表
loaded_encoding = json.loads(json_encoding)
# 转换为 tensor
tensor_encoding = torch.tensor(loaded_encoding) """


@api_view(["POST"])
@csrf_exempt
def get_frames(request):
    """人脸采集"""
    frames = request.data.get("frames")
    token = request.data.get("token")
    if not token:
        return Response(
            {"error": "Token is required."}, status=status.HTTP_400_BAD_REQUEST
        )
    start = time.time()

    #此处的方法可以替换为其他方法，只需要获取处理后得到的特征

    result = face_identity.manage_frames(frames)
    end = time.time()
    print(f"耗时：{end - start:.4f}")
    if result is not None:
        try:
            final_average_encoding_list = result.tolist()
            json_encoding = json.dumps(final_average_encoding_list)  # 转换为 JSON 字符串
            token_instance = Token.objects.get(key=token)
            user = token_instance.user
            user.identity_code = json_encoding  # 用赋值而非 update 方法
            user.save()  # 确保保存更改
            return Response(
                {"code": 0, "content": "信息采集成功"}, status=status.HTTP_200_OK
            )
        except:
            return Response(
                {"code": 1, "content": "数据采集失败，请稍后重试"},
                status=status.HTTP_200_OK,
            )
    else:
        return Response(
            {"code": 1, "content": "有效样本过少，请重新尝试人脸信息采集"},status=status.HTTP_200_OK
        )


@api_view(["POST"])
@csrf_exempt
def del_identity(request):
    """删除面部识别信息"""
    token = request.data.get("token")
    if not token:
        return Response({"code": 0, "msg": "信息校验出错！"}, status=status.HTTP_200_OK)
    token_instance = Token.objects.get(key=token)
    user = token_instance.user
    try:
        user.identity_code = None
        user.save()
    except:
        return Response(
            {"code": 0, "msg": "操作失败，服务器内部错误！"}, status=status.HTTP_200_OK
        )
    return Response(
        {"code": 1, "msg": "操作成功！面部数据已删除"},
        status=status.HTTP_200_OK,
    )
