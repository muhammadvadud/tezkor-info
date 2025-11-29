from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from model_bakery import baker


class CompanySelectionModel(AbstractBaseModel):
    continent = models.CharField(verbose_name=_("continent"), max_length=255)
    country = models.CharField(verbose_name=_("country"), max_length=255)
    region = models.CharField(verbose_name=_("region"), max_length=255)
    district = models.CharField(verbose_name=_("district"), max_length=255)
    letters = models.CharField(verbose_name=_("letters"), max_length=255)
    total_companies = models.IntegerField(verbose_name=_("total_companies"))
    ad_price = models.PositiveBigIntegerField(verbose_name=_("ad_price"))
    total_price = models.PositiveBigIntegerField(verbose_name=_("total_price"))

    def __str__(self):
        return str(self.pk)

    @classmethod
    def _baker(cls):
        return baker.make(cls)

    class Meta:
        db_table = "Company_selection"
        verbose_name = _("CompanySelectionModel")
        verbose_name_plural = _("CompanySelectionModels")
