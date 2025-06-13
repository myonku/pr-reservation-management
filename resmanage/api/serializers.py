from dataclasses import fields
from rest_framework import serializers
from resvation.models import time_sep, user, device, origin_resvation, approved_reservation


# Device Serializer  设备模型序列化器
class DeviceSerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField()
    class Meta:
        model = device
        fields = [
            "name",
            "state",
        ]

    def get_state(self, obj):
        return obj.get_state_display()

    def to_representation(self, instance):
        representation = super(DeviceSerializer, self).to_representation(instance)

        return representation

# 设备模型简易序列化器
class S_DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = device
        fields = [
            "name",
        ]

    def to_representation(self, instance):
        representation = super(S_DeviceSerializer, self).to_representation(instance)

        return representation


# 用户模型简易序列化器
class S_UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = [
            "username",
            "profile",
        ]

    def to_representation(self, instance):
        representation = super(S_UserSerializer, self).to_representation(instance)

        return representation


class S_APD_ResvationSerializer(serializers.ModelSerializer):

    state_apd = serializers.SerializerMethodField()

    class Meta:

        model = approved_reservation
        fields = [
            "id",
            "state_apd",
            "completed_time"
        ]

    def get_state_apd(self, obj):
        return obj.get_state_apd_display()

    def to_representation(self, instance):
        representation = super(S_APD_ResvationSerializer, self).to_representation(
                instance
            )
        if instance.completed_time is not None:
            representation["completed_time"] = instance.completed_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        return representation

# Reservation Serializer  预约申请记录模型序列化器
class ResvationSerializer(serializers.ModelSerializer):
    res_user = S_UserSerializer(many=False)
    audit_staff = S_UserSerializer(many=False)
    inviter = S_UserSerializer(many=False)
    device = S_DeviceSerializer(many=False)
    state = serializers.SerializerMethodField()
    apd_ori_resvation = S_APD_ResvationSerializer(many=True, read_only=True)
    class Meta:
        model = origin_resvation

        fields = [
            "id",
            "res_user",
            "audit_staff",
            "res_time",
            "audit_time",
            "res_start_time",
            "res_end_time",
            "state",
            "inviter",
            "device",
            "description",
            "res_dec_time",
            "apd_ori_resvation",
        ]

    def get_state(self, obj):
        return obj.get_state_display()

    def to_representation(self, instance):
        representation = super(ResvationSerializer, self).to_representation(instance)
        representation["res_time"] = instance.res_time.strftime("%Y-%m-%d %H:%M:%S")
        if instance.audit_time is not None:
            representation["audit_time"] = instance.audit_time.strftime("%Y/%m/%d %H:%M:%S")
        representation["res_start_time"] = instance.res_start_time.strftime(
            "%Y/%m/%d %H:%M"
        )
        representation["res_end_time"] = instance.res_end_time.strftime(
            "%Y/%m/%d %H:%M"
        )
        representation["res_dec_time"] = instance.res_dec_time.strftime(
            "%Y/%m/%d %H:%M"
        )

        return representation


# 预约申请记录模型简易序列化器
class S_ResvationSerializer(serializers.ModelSerializer):

    class Meta:
        model = origin_resvation
        fields = ["id",]

    def to_representation(self, instance):
        representation = super(S_ResvationSerializer, self).to_representation(instance)

        return representation


# 通过记录


# 面向用户预约申请记录模型序列化器


class UTR_APD_ResvationSerializer(serializers.ModelSerializer):

    state_apd = serializers.SerializerMethodField()

    class Meta:

        model = approved_reservation
        fields = ["state_apd", "completed_time"]

    def get_state_apd(self, obj):
        return obj.get_state_apd_display()

    def to_representation(self, instance):
        representation = super(UTR_APD_ResvationSerializer, self).to_representation(
            instance
        )
        if instance.completed_time is not None:
            representation["completed_time"] = instance.completed_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        return representation


class UTR_ResvationSerializer(serializers.ModelSerializer):
    res_user = S_UserSerializer(many=False)
    inviter = S_UserSerializer(many=False)
    device = S_DeviceSerializer(many=False)
    state = serializers.SerializerMethodField()
    apd_ori_resvation = UTR_APD_ResvationSerializer(many=True, read_only=True)

    class Meta:
        model = origin_resvation

        fields = [
            "res_user",
            "res_time",
            "audit_time",
            "res_start_time",
            "res_end_time",
            "state",
            "inviter",
            "device",
            "description",
            "res_dec_time",
            "apd_ori_resvation",
        ]

    def get_state(self, obj):
        return obj.get_state_display()

    def to_representation(self, instance):
        representation = super(UTR_ResvationSerializer, self).to_representation(
            instance
        )
        representation["res_time"] = instance.res_time.strftime("%Y-%m-%d %H:%M:%S")
        if instance.audit_time is not None:
            representation["audit_time"] = instance.audit_time.strftime(
                "%Y/%m/%d %H:%M:%S"
            )
        representation["res_start_time"] = instance.res_start_time.strftime(
            "%Y/%m/%d %H:%M"
        )
        representation["res_end_time"] = instance.res_end_time.strftime(
            "%Y/%m/%d %H:%M"
        )
        representation["res_dec_time"] = instance.res_dec_time.strftime(
            "%Y/%m/%d %H:%M"
        )

        return representation


class APD_ResvationSerializer(serializers.ModelSerializer):

    origin_resvation = ResvationSerializer(many=False)
    state_apd = serializers.SerializerMethodField()

    class Meta:

        model = approved_reservation
        fields = [
            "id",
            "origin_resvation",
            "completed_time",
            "state_apd",
        ]

    def get_state_apd(self, obj):
        return obj.get_state_apd_display()

    def to_representation(self, instance):
        representation = super(APD_ResvationSerializer, self).to_representation(
                instance
            )
        if instance.completed_time is not None:
            representation["completed_time"] = instance.completed_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        return representation


class Time_SepSerializer(serializers.ModelSerializer):
    max_resnum = serializers.SerializerMethodField()
    class Meta:
        model = time_sep
        fields = "__all__"

    def get_max_resnum(self, obj):
        return obj.get_max_resnum_display()

    def to_representation(self, instance):
        representation = super(Time_SepSerializer, self).to_representation(instance)
        representation["date"] = instance.date.strftime("%Y-%m-%d")
        if instance.updated_at is not None:
            representation["updated_at"] = instance.updated_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        return representation
