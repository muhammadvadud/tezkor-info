from django.contrib import admin
from unfold.admin import ModelAdmin

from core.apps.main.models import CategoryModel, CompanySelectionModel


@admin.register(CategoryModel)
class CategoryAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )


@admin.register(CompanySelectionModel)
class CompanySelectionModelAdmin(ModelAdmin):
    search_fields = ["id"]

    list_display = (
        "id",
        "__str__",
    )
