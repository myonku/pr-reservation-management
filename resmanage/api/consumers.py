from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.exceptions import StopConsumer
from django.utils import timezone
from channels.db import database_sync_to_async


class Identity_Consumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        raise StopConsumer()

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data["type"] == 10:
            print(data["data"])

        # 处理类型1的消息   请求特征向量数据
        elif data["type"] == 0:
            print("接收请求::获取匹配数据")
            await self.handle_type1(data)

        # 处理类型2的消息   面部匹配结果确认
        elif data["type"] == 1:
            print("接收请求::匹配确认更新")
            await self.handle_type2(data)

        # 处理类型3的消息   二维码匹配
        elif data["type"] == 2:
            print("接收请求::二维码匹配")
            await self.handle_type3(data)

        # 消息通知
        elif data["type"] == 11:
            """用户连接"""
            print("接收请求::用户连接")
            await self.handle_type11(data)

        elif data["type"] == 12:
            print("接收请求::用户确认")
            await self.handle_type12(data)

        elif data["type"] == 13:
            pass

    async def handle_type11(self, data):
        token = data["token"]
        data = await self.get_login_message(token)
        if data:
            result = {"type": 11,"result": data}
            await self.send(text_data=json.dumps(result))

    async def handle_type12(self, data):
        token = data["token"]
        user = await self.get_login_user(token)
        if data:
            await self.update_confirm_message(data, user)

    async def handle_type1(self, data):

        # 获取客户端发送的时间
        client_time = datetime.strptime(data.get("client_time"), "%Y-%m-%d %H:%M:%S")
        device = data.get("device")
        # 筛选符合条件的预约记录
        reservations = await self.get_reservations(client_time, device)
        # 构建返回的用户向量预约列表
        response_list = list(
            set(
                (
                    reservation["id"],  # 使用字典的键访问值
                    reservation["res_user__username"],  # 访问用户名
                    reservation["res_user__identity_code"],  # 访问身份代码
                )
                for reservation in reservations
            )
        )
        # 将结果发送回客户端
        await self.send(
            text_data=json.dumps(
                {"type": "type1_response", "reservations": response_list}
            )
            + "end"
        )

    @database_sync_to_async
    def get_reservations(self, client_time, idevice):
        # 筛选符合条件的预约记录
        from resvation.models import origin_resvation, device

        xdevice = device.objects.get(name=idevice)
        return list(
            origin_resvation.objects.filter(
                res_dec_time__gt=client_time,
                res_start_time__lte=client_time,
                state="2",
                device=xdevice,
            )
            .select_related("res_user")
            .values("id", "res_user__username", "res_user__identity_code")
        )

    async def handle_type2(self, data):

        # 获取匹配结果信息
        match_result = data.get("match_result")
        if match_result:
            match_time = timezone.now()  # 获取当前时间
            try:
                id = data.get("id")
                x = await self.get_origin_reservation(id)
                oce = x[0]
                username = x[1] if oce else None
                r = await self.update_approved_reservation(oce, match_time)
                if r == 1:
                    status = "success"
                else:
                    status = "empty"
            except:
                status = "error"
                username = None

            response = {
                "type": "type2_response",
                "username": username,
                "match_time": datetime.strftime(match_time, "%Y-%m-%d %H:%M:%S"),
                "status": status,
            }
        else:
            response = {
                "type": "type2_response",
                "status": "confirmed",
            }

        # 将结果发送回客户端
        await self.send(text_data=json.dumps(response) + "end")

    @database_sync_to_async
    def get_origin_reservation(self, id):
        """异步获取 origin_resvation 记录"""
        from resvation.models import origin_resvation
        x = origin_resvation.objects.get(id=int(id))
        user = x.res_user.username
        return x, user

    @database_sync_to_async
    def update_approved_reservation(self, oce, match_time):
        """异步更新 approved_reservation 记录"""
        from resvation.models import approved_reservation, origin_resvation

        if isinstance(oce, origin_resvation):
            # oce 是一个模型实例
            x = approved_reservation.objects.get(origin_resvation=oce)
            if x.state_apd == "3":
                return 0
            else:
                x.state_apd="3"
                x.completed_time=match_time
                x.save()
                return 1
        else:
            # oce 是一个 QuerySet
            c = 0
            for i in oce:
                x = approved_reservation.objects.get(origin_resvation=i)
                if x.state_apd == "3":
                    continue
                else:
                    x.state_apd="3"
                    x.completed_time=match_time
                    x.save()
                    c += 1
            if c > 0:
                return 1
            else:
                return 0

    async def handle_type3(self, data):

        idevice = data.get("device")
        qrcode = data.get("qrcode")
        client_time = data.get("client_time")
        match_time = datetime.now()
        fr = await self.get_user_to_resvation(qrcode, client_time, idevice)
        resvations = fr[0]
        username = fr[1]
        if resvations:
            try:
                r = await self.update_approved_reservation(resvations, match_time)
                status = "success" if r == 1 else "empty"
            except:
                status = "error"
        else:
            status = "none"

        response = {
            "type": "type3_response",
            "status": status,
            "username": username,
            "match_time": datetime.strftime(match_time, "%Y-%m-%d %H:%M:%S"),
        }
        await self.send(text_data=json.dumps(response) + "end")

    @database_sync_to_async
    def get_user_to_resvation(self, qrcode, client_time, idevice):
        """异步获取 origin_resvation 记录"""
        from resvation.models import origin_resvation, user, device

        iuser = user.objects.get(qr_data=qrcode)
        xdevice = device.objects.get(name=idevice)
        time = datetime.strptime(client_time, "%Y-%m-%d %H:%M:%S")
        resvations = origin_resvation.objects.filter(
            res_user=iuser,
            res_dec_time__gt=time,
            res_start_time__lte=time,
            state="2",
            device=xdevice,
        )
        name = iuser.username if iuser else ""

        return resvations, name

    @database_sync_to_async
    def get_login_user(self, token):
        from rest_framework.authtoken.models import Token

        if not token:
            return 0
        token_instance = Token.objects.get(key=token)
        iuser = token_instance.user
        return iuser

    @database_sync_to_async
    def get_login_message(self, token):
        from resvation.models import (
            origin_resvation,
            approved_reservation,
            time_sep,
        )
        from rest_framework.authtoken.models import Token

        if not token:
            return 0
        token_instance = Token.objects.get(key=token)
        iuser = token_instance.user

        last_login = iuser.last_login
        changed_resvations_1 = origin_resvation.objects.filter(
            res_user=iuser, msg_phase=3, state="2"
        ).count()
        changed_resvations_2 = origin_resvation.objects.filter(
            res_user=iuser, msg_phase=3, state="3"
        ).count()
        changed_resvations_3 = origin_resvation.objects.filter(
            res_user=iuser, msg_phase=3, state="4"
        ).count()
        if_time_changed = time_sep.objects.filter(
            date__gt=last_login,
            updated_at__gt=last_login,
        ).count()
        changed_apd1 = approved_reservation.objects.filter(
            msg_phase=2, origin_resvation__res_user=iuser
        ).count()
        changed_apd2 = approved_reservation.objects.filter(
            msg_phase=3, origin_resvation__res_user=iuser
        ).count()
        return (
            changed_resvations_1,
            changed_resvations_2,
            changed_resvations_3,
            if_time_changed,
            changed_apd1,
            changed_apd2
        )

    @database_sync_to_async
    def update_confirm_message(self, data, user):
        from resvation.models import (
            origin_resvation,
            approved_reservation,
        )
        typex = data["typex"]
        if typex == 1:
            origin_resvation.objects.filter(
                res_user=user, msg_phase=3, state__in=["2", "3", "4"]
            ).update(msg_phase=4)
        elif typex == 2:
            approved_reservation.objects.filter(
                msg_phase__in=[2, 3], origin_resvation__res_user=user
            ).update(msg_phase=4)
