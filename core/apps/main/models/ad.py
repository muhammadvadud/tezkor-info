from calendar import month

from django_core.models import AbstractBaseModel
from model_bakery import baker
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.apps.main.choices import PaymentsTypeChoice, PaymentsStatusChoice


class AdModel(AbstractBaseModel):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_("name"), max_length=255)
    description = models.TextField(verbose_name=_("description"))
    total_view_count = models.PositiveIntegerField(verbose_name=_("view count"), default=0)
    types = models.ManyToManyField("main.CategoryModel", verbose_name=_("types"))
    is_referral_payments = models.BooleanField(default=False, verbose_name=_("is referral payments"))
    total_price = models.BigIntegerField(verbose_name=_("total price"), default=0)
    payments_type = models.CharField(max_length=255, choices=PaymentsTypeChoice, default=PaymentsTypeChoice.OTHER,
                                     verbose_name=_("payments type"))
    company_selections = models.ManyToManyField("main.CompanySelectionModel", verbose_name=_("company selections"))
    status = models.CharField(max_length=255, verbose_name=_("status"), choices=PaymentsStatusChoice,
                              default=PaymentsStatusChoice.PENDING)


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
