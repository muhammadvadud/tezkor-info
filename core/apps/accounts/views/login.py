import uuid
from typing import Type

from core.services import UserService, SmsService
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_core import exceptions
from drf_spectacular.utils import extend_schema
from rest_framework import status, throttling, request
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import GenericViewSet
from django_core.mixins import BaseViewSetMixin
from rest_framework.decorators import action
from ..serializers import (
    OTPLoginSerializer,
    OTPConfirmSerializer,
    OTPResendSerializer
)
from rest_framework.permissions import AllowAny


@extend_schema(tags=["Login"])
class LoginView(BaseViewSetMixin, GenericViewSet, UserService):
    throttle_classes = [throttling.UserRateThrottle]
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        match self.action:
            case "send_code":
                return OTPLoginSerializer
            case "confirm":
                return OTPConfirmSerializer
            case "resend":
                return OTPResendSerializer
            case _:
                return OTPLoginSerializer

    @action(methods=["POST"], detail=False, url_path="send_code")
    def send_code(self, request):
        """
            Login SMS Send
        """
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.data
        phone = data.get("phone")
        self.send_confirmation(phone)
        return Response(
            {"detail": _("Sms %(phone)s raqamiga yuborildi") % {"phone": phone}},
            status=status.HTTP_202_ACCEPTED,
        )

    @extend_schema(summary="Login code confirm.", description="Login code confirm")
    @action(methods=["POST"], detail=False, url_path="confirm")
    def confirm(self, request):
        """
        Login Code Confirm
        """
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.data
        phone, code = data.get("phone"), data.get("code")
        try:
            if SmsService.check_confirm(phone, code=code):
                token = self.validate_user(get_user_model().objects.filter(phone=phone).first())
                return Response(
                    data={
                        "detail": _("Tasdiqlash ko'di qabul qilindi"),
                        "token": token,
                    },
                    status=status.HTTP_202_ACCEPTED,
                )
        except exceptions.SmsException as e:
            raise PermissionDenied(e)  # Response exception for APIException
        except Exception as e:
            raise PermissionDenied(e)  # Api exception for APIException

    @action(methods=["POST"], detail=False, url_path="resend")
    def resend(self, rq: Type[request.Request]):
        ser = self.get_serializer(data=rq.data)
        ser.is_valid(raise_exception=True)
        phone = ser.data.get("phone")
        self.send_confirmation(phone)
        return Response({"detail": _("Sms %(phone)s raqamiga yuborildi") % {"phone": phone}})
