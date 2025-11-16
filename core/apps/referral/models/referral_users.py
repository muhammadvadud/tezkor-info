from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from model_bakery import baker
from django.contrib.auth import get_user_model


class ReferralUsersModel(AbstractBaseModel):
    """
    Referal orqali qo'shilgan userlarni saqlaydigan model
    """
    referral_owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="referral_owner",
                                       verbose_name=_("Referral Owner"))
    referral_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="referral_user",
                                      verbose_name=_("Referral User"))

    def __str__(self):
        return str(self.pk)

    @classmethod
    def _baker(cls):
        return baker.make(cls)

    class Meta:
        db_table = "referral_users"
        verbose_name = _("ReferralUsersModel")
        verbose_name_plural = _("ReferralUsersModels")
