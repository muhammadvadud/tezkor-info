from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from core.apps.main.models import AdModel
from ..choices.referral_history_choice import ReferralHistoryType
from ..models.referral import ReferralModel
from model_bakery import baker
from django.contrib.auth import get_user_model


class ReferralHistoryModel(AbstractBaseModel):
    type = models.CharField(max_length=255, choices=ReferralHistoryType, verbose_name=_("Type"))
    amount = models.PositiveBigIntegerField(verbose_name=_("Amount"))
    referral = models.ForeignKey(ReferralModel, verbose_name=_("Referral"), on_delete=models.CASCADE, null=True,
                                 blank=True)
    ad = models.ForeignKey(AdModel, verbose_name=_("Ad"), on_delete=models.CASCADE)
    owner = models.ForeignKey(get_user_model(), verbose_name=_("Owner"), on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)

    @classmethod
    def _baker(cls):
        return baker.make(cls)

    class Meta:
        db_table = "ReferralHistory"
        verbose_name = _("ReferralHistoryModel")
        verbose_name_plural = _("ReferralHistoryModels")
