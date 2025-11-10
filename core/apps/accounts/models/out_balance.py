from django.db import models
from django_core.models.base import AbstractBaseModel
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from core.apps.main.models import AdModel


class OutBalance(AbstractBaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_("User"))
    balance = models.PositiveBigIntegerField(verbose_name=_("Balance"))
    ad = models.ForeignKey(AdModel, on_delete=models.CASCADE, verbose_name=_("Ad"))

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = "out_balance"
        verbose_name = _("OutBalance")
        verbose_name_plural = _("OutBalance")
