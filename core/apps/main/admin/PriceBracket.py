from unfold.admin import ModelAdmin

from core.apps.main.models import PriceBracketModel
from django.contrib import admin


@admin.register(PriceBracketModel)
class PricebracketAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
