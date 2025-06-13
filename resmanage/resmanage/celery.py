from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "resmanage.settings")  # 设置django环境


app = Celery("resmanage")


app.config_from_object(
    "django.conf:settings", namespace="CELERY"
)                                                    #  使用CELERY_ 作为前缀，在settings中写配置

app.autodiscover_tasks(["resvation.celery_tasks"])  # 发现任务文件每个app下的task


app.conf.beat_schedule = {
    "update-reservation-status-every-hour": {
        "task": "resvation.celery_tasks.update_reservation_status",  # 使用任务的完整路径
        "schedule": crontab(minute=0, hour="*"),  # 每小时整点执行
    },
    "run-daily-task-at-midnight": {
        "task": "resvation.celery_tasks.auto_create_timesep",  # 使用新增任务的完整路径
        "schedule": crontab(minute=0, hour=0),  # 每天 0 点整执行
    },
}
