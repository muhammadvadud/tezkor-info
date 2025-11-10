from calendar import month

from django_core.models import AbstractBaseModel
from model_bakery import baker
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.apps.main.models import ActivateTypesModel
from core.apps.main.choices import PaymentsTypeChoice


class AdModel(AbstractBaseModel):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_("name"), max_length=255)
    description = models.TextField(verbose_name=_("description"))
    total_view_count = models.PositiveIntegerField(verbose_name=_("view count"), default=0)
    types = models.ManyToManyField(ActivateTypesModel, verbose_name=_("types"))
    is_referral_payments = models.BooleanField(default=False, verbose_name=_("is referral payments"))
    total_price = models.BigIntegerField(verbose_name=_("total price"), default=0)
    letters = models.CharField(max_length=255, verbose_name=_("letters"), blank=True, default="")
    payments_type = models.CharField(max_length=255, choices=PaymentsTypeChoice, default=PaymentsTypeChoice.OTHER,
                                     verbose_name=_("payments type"))

    def __str__(self):
        return str(self.pk)

    @classmethod
    def _baker(cls):
        return baker.make(cls)

    class Meta:
        db_table = "ad"
        verbose_name = _("AdModel")
        verbose_name_plural = _("AdModels")


class AdFilesModel(AbstractBaseModel):
    ad = models.ForeignKey(AdModel, verbose_name=_("ad"), on_delete=models.CASCADE, related_name="files")
    file = models.FileField(verbose_name=_("file"), upload_to="ads/files/")

    def __str__(self):
        return str(self.pk)

    @classmethod
    def _baker(cls):
        return baker.make(cls)

    class Meta:
        db_table = "ad_files"
        verbose_name = _("AdFilesModel")
        verbose_name_plural = _("AdFilesModels")


class AdCountries(AbstractBaseModel):
    ad = models.ForeignKey(AdModel, verbose_name=_("ad"), on_delete=models.CASCADE, related_name="countries")
    continent = models.CharField(max_length=255, verbose_name=_("continent"))
    country = models.CharField(max_length=255, verbose_name=_("country"))
    region = models.CharField(max_length=255, verbose_name=_("region"))
    city = models.CharField(max_length=255, verbose_name=_("city"))
    total_view = models.PositiveIntegerField(verbose_name=_("view count"), default=0)
    price = models.BigIntegerField(verbose_name=_("price"))

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = "ad_countries"
        verbose_name = _("AdCountries")
        verbose_name_plural = _("AdCountries")
