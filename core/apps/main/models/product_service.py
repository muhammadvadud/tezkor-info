from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from model_bakery import baker


class ProductServiceModel(AbstractBaseModel):
    title = models.CharField(verbose_name=_("title"), max_length=255)
    description = models.TextField(verbose_name=_("description"))
    company = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="product_service_company",
        verbose_name=_("company"),
    )
    category = models.ForeignKey("main.CategoryModel", on_delete=models.CASCADE, verbose_name=_("category"))

    def __str__(self):
        return str(self.pk)

    @classmethod
    def _baker(cls):
        return baker.make(cls)

    class Meta:
        db_table = "ProductService"
        verbose_name = _("ProductServiceModel")
        verbose_name_plural = _("ProductServiceModels")


class ProductServiceFilesModel(AbstractBaseModel):
    file = models.FileField(verbose_name=_("file"), upload_to="files")
    service = models.ForeignKey(ProductServiceModel, on_delete=models.CASCADE,
                                verbose_name=_("product service"), related_name="files", )

    def __str__(self):
        return str(self.pk)

    @classmethod
    def _baker(cls):
        return baker.make(cls)

    class Meta:
        db_table = "ProductServiceFiles"
        verbose_name = _("ProductServiceFiles")
        verbose_name_plural = _("ProductServiceFiles")
