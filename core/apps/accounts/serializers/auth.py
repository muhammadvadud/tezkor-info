from config.env import env
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework import exceptions, serializers
from core.apps.accounts.models.region import Country, Region, District

OTP_SIZE = env.int("OTP_SIZE", 4)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=255)
    country = serializers.CharField(max_length=255, required=False, allow_blank=True)
    region = serializers.CharField(max_length=255, required=False, allow_blank=True)
    district = serializers.CharField(max_length=255, required=False, allow_blank=True)
    referral = serializers.CharField(max_length=255, required=False, allow_blank=True)

    def validate_phone(self, value):
        user = get_user_model().objects.filter(phone=value, validated_at__isnull=False)
        if user.exists():
            raise exceptions.ValidationError(_("Phone number already registered."), code="unique")
        return value

    class Meta:
        model = get_user_model()
        fields = ["company_name", "stir", "director_full_name",
                  "person_type", "activate_types", "country", "region", "district", "phone", "referral"]
        extra_kwargs = {
            "referral": {"required": False},
        }


class ConfirmSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=OTP_SIZE, min_length=OTP_SIZE)
    phone = serializers.CharField(max_length=255)
    tg_id = serializers.CharField(max_length=255, required=False)


class ResetPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=255)

    def validate_phone(self, value):
        user = get_user_model().objects.filter(phone=value)
        if user.exists():
            return value

        raise serializers.ValidationError(_("User does not exist"))


class ResetConfirmationSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=OTP_SIZE, max_length=OTP_SIZE)
    phone = serializers.CharField(max_length=255)

    def validate_phone(self, value):
        user = get_user_model().objects.filter(phone=value)
        if user.exists():
            return value
        raise serializers.ValidationError(_("User does not exist"))


class ResendSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=255)
