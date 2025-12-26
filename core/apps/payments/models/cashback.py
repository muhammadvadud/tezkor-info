from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from model_bakery import baker

from core.apps.main.models import AdModel


class CashbackModel(AbstractBaseModel):
    ad = models.ForeignKey(AdModel, verbose_name=_("Ad"), on_delete=models.CASCADE, related_name="cashback")
    user = models.ForeignKey(get_user_model(), verbose_name=_("User"), on_delete=models.CASCADE,
                             related_name="cashback")
    amount = models.PositiveBigIntegerField(verbose_name=_("Amount"), default=0)
    percent = models.PositiveSmallIntegerField(verbose_name=_("Percent"), default=0)

    def __str__(self):
        return str(self.pk)

    @classmethod
    def _baker(cls):
        return baker.make(cls)

    class Meta:
        db_table = "cashback"
        verbose_name = _("CashbackModel")
        verbose_name_plural = _("CashbackModels")


class CashbackPercentModel(AbstractBaseModel):
    percent = models.PositiveSmallIntegerField(verbose_name=_("Amount"), default=0)

    def __str__(self):
        return str(self.percent)

    class Meta:
        db_table = "cashback_percent"
        verbose_name = _("CashbackPercent")
        verbose_name_plural = _("CashbackPercents")
