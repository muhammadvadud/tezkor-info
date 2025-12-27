from django_core.models.base import AbstractBaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Country(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Country name"))
    code = models.CharField(max_length=100, verbose_name=_("Country code"), null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "country"
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")


class Region(AbstractBaseModel):
    country = models.ForeignKey(Country, verbose_name=_("Country"), on_delete=models.PROTECT, related_name="region")
    name = models.CharField(max_length=255, verbose_name=("Region Name"))
    code = models.CharField(max_length=100, verbose_name=_("Region code"), null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "region"
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")


class District(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=("District Name"))
    region = models.ForeignKey(Region, on_delete=models.PROTECT, verbose_name=_("Region"), related_name="districts")
    code = models.CharField(max_length=100, verbose_name=_("Disrict code"), null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "district"
        verbose_name = _("District")
        verbose_name_plural = _("Districts")
