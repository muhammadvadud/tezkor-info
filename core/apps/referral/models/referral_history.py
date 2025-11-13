from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from model_bakery import baker


class ReferralHistoryModel(AbstractBaseModel):
    amount = models.PositiveBigIntegerField(verbose_name=_("Amount"))


    def __str__(self):
        return str(self.pk)

    @classmethod
    def _baker(cls):
        return baker.make(cls)

    class Meta:
        db_table = "ReferralHistory"
        verbose_name = _("ReferralHistoryModel")
        verbose_name_plural = _("ReferralHistoryModels")
