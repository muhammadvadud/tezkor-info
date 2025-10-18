from django_core.models import AbstractBaseModel
from model_bakery import baker
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.apps.main.models import ActivateTypesModel


class AdModel(AbstractBaseModel):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_("name"), max_length=255)
    description = models.TextField(verbose_name=_("description"))
    view_count = models.PositiveIntegerField(verbose_name=_("view count"), default=0)
    types = models.ManyToManyField(ActivateTypesModel, verbose_name=_("types"))

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
