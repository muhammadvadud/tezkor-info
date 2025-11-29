from django.db import models
from django_core.models.base import AbstractBaseModel
from django.utils.translation import gettext_lazy as _


class UserTgIds(AbstractBaseModel):
    tg_id = models.BigIntegerField(verbose_name=_("id"))

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = "user_tg_ids"
        verbose_name = _("User TgIds")
        verbose_name_plural = _("User TgIds")
