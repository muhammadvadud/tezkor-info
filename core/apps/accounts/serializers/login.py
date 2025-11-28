from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from config.env import env

OTP_SIZE = env.int("OTP_SIZE", 4)


class OTPLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)

    def validate_phone(self, value):
        user = get_user_model().objects.filter(phone=value)
        if user.exists():
            return value

        raise serializers.ValidationError(_("User does not exist"))


class OTPConfirmSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=OTP_SIZE, min_length=OTP_SIZE)
    phone = serializers.CharField(max_length=255)
    tg_id = serializers.CharField(max_length=255, required=False)


class OTPResendSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=OTP_SIZE, min_length=OTP_SIZE)
