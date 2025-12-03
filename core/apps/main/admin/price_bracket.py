from django.contrib import admin
from unfold.admin import ModelAdmin

from core.apps.main.models import PriceBracket


@admin.register(PriceBracket)
class PriceBracketAdmin(ModelAdmin):
    search_fields = ["id"]
    list_display = (
        "id",
        "__str__",
    )
