import datetime
from django.db import models
from django.db.models import F
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.utils.crypto import get_random_string
from api.utils import Res_Manager
# Create your models here.
MEDIA_ADDR = "http://localhost:8000/media/"


STATE = (("1", "待审核"), ("2", "已通过"), ("3", "未通过"), ("4", "已过期"))
STATE_APD = (("1", "未生效"), ("2", "待认证"), ("3", "已认证"), ("4", "已过期"))
STATE_DEVICE =(("1", "在线"), ("2", "设备异常"), ("3", "掉线"))

def get_following_datetime():
    return datetime.datetime.now() + datetime.timedelta(days=3)


# 用户模型
class user(AbstractUser):    

    username = models.CharField(max_length=20, verbose_name="用户名", unique=True)
    profile = ProcessedImageField(
        upload_to="avatar/",
        default="avatar/default.jpg",
        verbose_name="头像",
        processors=[ResizeToFill(150, 150)],
    )
    common_staff = models.BooleanField(verbose_name="普通员工", default=False)
    if_staff = models.BooleanField(verbose_name="后台员工", default=False)
    identity_code = models.TextField(verbose_name="人脸识别码", null=True, blank=True)
    qr_data = models.CharField(max_length=100, verbose_name="二维码", blank=True, null=True)
    phone_number = models.CharField(blank=True, null=True, verbose_name="手机号", max_length=12)

    def update_qrcode(self):
        qr_data = (
            f"{self.username}-{self.id}-{get_random_string(12)}"  # 生成二维码数据
        )
        self.qr_data = qr_data
        self.save()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

#  门禁通道（设备）模型
class device(models.Model):
    name = models.CharField(
        verbose_name="门禁通道",
        unique=True,
        max_length=30,
    )

    state = models.CharField(
        verbose_name="状态",
        choices = STATE_DEVICE,
        default="1",
        max_length=20,
    )   

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "门禁通道（设备）"
        verbose_name_plural = verbose_name

# 预约申请模型
class origin_resvation(models.Model):

    res_user = models.ForeignKey(
        related_name="res_user",
        to=user,
        verbose_name="预约用户",
        on_delete=models.DO_NOTHING
    )
    audit_staff = models.ForeignKey(
        to=user,
        related_name="res_audit",
        verbose_name="审核人",
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING
    )
    inviter = models.ForeignKey(
        to=user,
        null=True,
        blank=True,
        related_name="res_inviter",
        verbose_name="邀请人",
        on_delete=models.DO_NOTHING,
    )
    res_time = models.DateTimeField(
        verbose_name="预约申请时间",
        auto_now_add=True,
    )
    res_time_only = models.TimeField(
        verbose_name="预约申请时间（时间部分）", null=True, blank=True
    )
    audit_time = models.DateTimeField(verbose_name="审核时间", blank=True, null=True)
    res_start_time = models.DateTimeField(
        verbose_name="预约起始时间",
    )
    res_start_time_only = models.TimeField(
        verbose_name="预约起始时间（时间部分）", null=True, blank=True
    )
    res_dec_time = models.DateTimeField(
        verbose_name="预约结束时间", null=True, blank=True,
    )
    res_end_time = models.DateTimeField(
        verbose_name="申请失效时间",
        default=get_following_datetime,
    )
    state = models.CharField(
        max_length=10, verbose_name="状态", choices=STATE, default="1"
    )
    device = models.ForeignKey(
        to=device,
        verbose_name="门禁通道",
        related_name="res_device",
        on_delete=models.DO_NOTHING,
    )
    description = models.TextField(
        verbose_name="备注"
    )
    msg_phase = models.IntegerField(verbose_name="消息周期阶段", default=1)

    #  msg_phase 1-新建未确认 2-新建已确认 3-更改未确认 4-更改已确认

    def save(self, *args, **kwargs):
        if not self.res_dec_time:
            temp = str(self.res_start_time)
            format = r"%Y-%m-%d %H:%M:%S"
            time0 = datetime.datetime.strptime(temp, format)
            time = time0 + datetime.timedelta(hours=2,minutes=59, seconds=59)
            self.res_dec_time = time
            self.res_end_time = min(time, self.res_end_time)
        #
        self.res_start_time_only = self.res_start_time.time()
        if self.res_time:
            self.res_time_only = self.res_time.time()
        else:
            self.res_time_only = datetime.datetime.now().time()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.res_user.username}"

    objects = Res_Manager()

    class Meta:
        verbose_name = "预约申请记录"
        verbose_name_plural = verbose_name


# 已通过申请（待通过记录）模型
class approved_reservation(models.Model):
    msg_phase = models.IntegerField(verbose_name="消息周期阶段", default=1)
    #  msg_phase 1-新建未确认 2-生效阶段 3-过期阶段 4-过期已确认

    state_apd = models.CharField(
        max_length=10,
        verbose_name="状态",
        choices=STATE_APD,
        default="1",
    )
    origin_resvation = models.ForeignKey(
        to=origin_resvation, related_name="apd_ori_resvation", verbose_name="已通过申请",on_delete=models.DO_NOTHING,
    )
    completed_time = models.DateTimeField(
        verbose_name="通过时间",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.id} - {self.origin_resvation.res_user.username}"

    class Meta:
        verbose_name = "预约通过记录"
        verbose_name_plural = verbose_name


# 预约时段分配

class time_sep(models.Model):

    date = models.DateField(default=get_following_datetime, verbose_name="日期")
    transform_num = models.IntegerField(verbose_name="修改次数", default=0)
    if_valid = models.BooleanField(verbose_name="当日可预约",default=True)
    interval = models.IntegerField(verbose_name="间隔长度", choices=((2,2),(3,3),(4,4)), default=2)
    max_resnum = models.IntegerField(
        verbose_name="最大预约数量",
        choices=((0, 99999998), (1, 10), (2, 50), (3, 100), (4, 99999999)),
        default=0,
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="上次更新")
    # 整点时刻字段（每个整点时刻用布尔值表示是否可预约）
    hour_0 = models.BooleanField(default=False, verbose_name="00:00")
    hour_1 = models.BooleanField(default=False, verbose_name="01:00")
    hour_2 = models.BooleanField(default=False, verbose_name="02:00")
    hour_3 = models.BooleanField(default=False, verbose_name="03:00")
    hour_4 = models.BooleanField(default=False, verbose_name="04:00")
    hour_5 = models.BooleanField(default=False, verbose_name="05:00")
    hour_6 = models.BooleanField(default=False, verbose_name="06:00")
    hour_7 = models.BooleanField(default=True, verbose_name="07:00")
    hour_8 = models.BooleanField(default=True, verbose_name="08:00")
    hour_9 = models.BooleanField(default=True, verbose_name="09:00")
    hour_10 = models.BooleanField(default=True, verbose_name="10:00")
    hour_11 = models.BooleanField(default=False, verbose_name="11:00")
    hour_12 = models.BooleanField(default=False, verbose_name="12:00")
    hour_13 = models.BooleanField(default=True, verbose_name="13:00")
    hour_14 = models.BooleanField(default=True, verbose_name="14:00")
    hour_15 = models.BooleanField(default=True, verbose_name="15:00")
    hour_16 = models.BooleanField(default=True, verbose_name="16:00")
    hour_17 = models.BooleanField(default=True, verbose_name="17:00")
    hour_18 = models.BooleanField(default=True, verbose_name="18:00")
    hour_19 = models.BooleanField(default=False, verbose_name="19:00")
    hour_20 = models.BooleanField(default=False, verbose_name="20:00")
    hour_21 = models.BooleanField(default=False, verbose_name="21:00")
    hour_22 = models.BooleanField(default=False, verbose_name="22:00")
    hour_23 = models.BooleanField(default=False, verbose_name="23:00")

    def __str__(self):
        return f"{self.date}"

    class Meta:
        verbose_name = "预约时段分配"
        verbose_name_plural = verbose_name
