from datetime import datetime

from core.services import sms
from django.contrib.auth import get_user_model, hashers
from django.utils.translation import gettext as _
from django_core import exceptions
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt import tokens
from core.apps.accounts.models.region import District, Region, Country
from django.db import transaction


class UserService(sms.SmsService):
    def get_token(self, user):
        refresh = tokens.RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def create_user(self, data):
        person_type = data.get("person_type")

        with transaction.atomic():
            country = data.get("country")
            region = data.get("region")
            district = data.get("district")

            country_obj = region_obj = district_obj = None

            if person_type == "legal_entity":
                country_obj, _ = Country.objects.get_or_create(name=country)
                region_obj, _ = Region.objects.get_or_create(name=region, country=country_obj)
                district_obj, _ = District.objects.get_or_create(name=district, region=region_obj)

            common_defaults = {
                "first_name": data.get("first_name"),
                "last_name": data.get("last_name"),
                "person_type": person_type,
            }

            if person_type == "legal_entity":
                common_defaults.update({
                    "district": district_obj,
                    "company_name": data.get("company_name"),
                    "stir": data.get("stir"),
                    "director_full_name": data.get("director_full_name"),
                })

            user, created = get_user_model().objects.update_or_create(
                phone=data["phone"],
                defaults=common_defaults,
            )
            if "activate_types" in data:
                user.activate_types.set(data["activate_types"])
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
