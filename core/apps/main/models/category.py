from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from model_bakery import baker


class CategoryModel(AbstractBaseModel):
    name = models.CharField(verbose_name=_("name"), max_length=255)
    code = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    level = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(null=True, blank=True)
    is_leaf = models.BooleanField(default=True)
    icon_name = models.CharField(
        verbose_name=_("icon name"),
        max_length=255,
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.pk)

    @classmethod
    def _baker(cls):
        return baker.make(cls)

    class Meta:
        db_table = "category"
        verbose_name = _("CategoryModel")
        verbose_name_plural = _("CategoryModels")
