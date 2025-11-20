from django.contrib import admin
from unfold.admin import ModelAdmin

from core.apps.main.models import PriceCountryModel


@admin.register(PriceCountryModel)
class PriceCountryAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
