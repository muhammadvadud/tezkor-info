from datetime import datetime

from core.services import sms
from django.contrib.auth import get_user_model, hashers
from django.utils.translation import gettext as _
from django_core import exceptions
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt import tokens
from core.apps.referral.tasks import user_add_for_referral
from core.services.get_user_all_data import get_user_all_data
from rest_framework.exceptions import ValidationError
from core.services.find_category_for_oked import find_category_by_oked
from core.apps.accounts.choices import PersonTypeChoice


class UserService(sms.SmsService):
    def get_token(self, user):
        refresh = tokens.RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def create_user(self, data):
        referral = data.get("referral")

        try:
            user_data = get_user_all_data(data['stir'])
        except ValueError as e:
            if str(e) == "ERR_USER_NOT_FOUND_404":
                raise ValidationError("Bunday korxona mavjud emas")
            else:
                raise

        category = find_category_by_oked(user_data["oked"])

        user, created = get_user_model().objects.update_or_create(
            phone=data["phone"],
            defaults={
                "person_type": PersonTypeChoice.LEGAL_ENTITY,
                "district": user_data["district"],
                "company_name": user_data["company_name"],
                "stir": data["stir"],
                "director_full_name": user_data["director_full_name"],
            }
        )

        if category:
            user.activate_types.set([category])
        if referral:
            user.referral = referral

        user.set_unusable_password()
        user.save()

        return user

    def send_confirmation(self, phone) -> bool:
        try:
            self.send_confirm(phone)
            return True
        except exceptions.SmsException as e:
            raise PermissionDenied(_("Qayta sms yuborish uchun kuting: {}").format(e.kwargs.get("expired")))
        except Exception:
            raise PermissionDenied(_("Serverda xatolik yuz berdi"))

    def validate_user(self, user) -> dict:
        """
        Create user if user not found
        """
        if user.validated_at is None:
            user.validated_at = datetime.now()
        user_add_for_referral(user)
        user.save()
        token = self.get_token(user)
        return token

    def is_validated(self, user) -> bool:
        """
        User is validated check
        """
        if user.validated_at is not None:
            return True
        return False

    def change_password(self, phone, password):
        """
        Change password
        """
        user = get_user_model().objects.filter(phone=phone).first()
        user.set_password(password)
        user.save()
