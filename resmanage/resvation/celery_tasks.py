import datetime
from celery import shared_task
from resvation.models import approved_reservation, origin_resvation, time_sep
from django.db.models import Q


@shared_task
def update_reservation_status():
    now = datetime.datetime.now()

    # 当前整点时间
    current_hour = now.replace(minute=0, second=0, microsecond=0)

    # 1. 未到预约起始时间，状态保持默认
    # 2. 在预约起始时间和预约结束时间之间，状态更改为待认证
    # 3. 超过预约结束时间，状态更改为已过期

    # 更新"未生效"的状态
    approved_reservation.objects.filter(
        Q(origin_resvation__res_start_time__gt=current_hour) & Q(state_apd="1")
    ).update(
        state_apd="1",
    )  # 保持未生效

    # 更新在预约起始时间和预约结束时间之间的状态
    approved_reservation.objects.filter(
        Q(origin_resvation__res_start_time__lte=now)
        & Q(origin_resvation__res_dec_time__gt=current_hour)
        & Q(state_apd="1")
    ).update(
        state_apd="2", msg_phase=2
    )  # 改为待认证

    # 更新超过预约结束时间的状态
    approved_reservation.objects.filter(
        Q(origin_resvation__res_dec_time__lt=current_hour)
        & Q(state_apd__in=["1", "2"])  # 只更新未生效和待认证
    ).update(
        state_apd="4", msg_phase=3
    )  # 改为已过期

    origin_resvation.objects.filter(
        res_end_time__lt=current_hour, state="1"  # 只更新待审核
    ).update(
        state="4", msg_phase=3
    )  # 改为已过期


@shared_task
def auto_create_timesep():
    for i in range(1, 12):
        day = datetime.date.today() + datetime.timedelta(days=i)
        if not time_sep.objects.filter(date=day).exists():
            time_sep.objects.create(date=day)
        else:
            continue
