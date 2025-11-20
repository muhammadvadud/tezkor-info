from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from model_bakery import baker
from core.apps.accounts.models.region import Country


class PriceCountryModel(AbstractBaseModel):
    country = models.OneToOneField(Country, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.country.name}: {self.price}"

    @classmethod
    def _baker(cls):
        return baker.make(cls)

    class Meta:
        db_table = "PriceCountry"
        verbose_name = _("PriceCountryModel")
        verbose_name_plural = _("PriceCountryModels")
