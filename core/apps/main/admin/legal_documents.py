from unfold.admin import ModelAdmin

from core.apps.main.models import LegalDocumentsModels
from django.contrib import admin


@admin.register(LegalDocumentsModels)
class LegalDocumentsAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
