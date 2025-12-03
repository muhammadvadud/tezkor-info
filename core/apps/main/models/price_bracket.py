from django.db import models
from django_core.models.base import AbstractBaseModel
from django.utils.translation import gettext_lazy as _


class PriceBracket(AbstractBaseModel):
    min_person = models.PositiveIntegerField(verbose_name=_("min_person"))
    max_person = models.PositiveIntegerField(verbose_name=_("max_person"))
    price = models.PositiveBigIntegerField(verbose_name=_("price"))

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = "price_bracket"  
        verbose_name = _("PriceBracket")
        verbose_name_plural = _("PriceBracket")
