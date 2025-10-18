from unfold.admin import ModelAdmin

from core.apps.main.models import ActivateTypesModel
from django.contrib import admin


@admin.register(ActivateTypesModel)
class ActivateTypesAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
