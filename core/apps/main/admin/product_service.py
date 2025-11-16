from django.contrib import admin
from unfold.admin import ModelAdmin

from core.apps.main.models import ProductServiceModel, ProductServiceFilesModel


class ProductServiceFilesInlineAdmin(admin.TabularInline):
    model = ProductServiceFilesModel
    extra = 1


@admin.register(ProductServiceModel)
class ProductServiceAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
    inlines = [ProductServiceFilesInlineAdmin]
