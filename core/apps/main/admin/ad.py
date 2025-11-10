from unfold.admin import ModelAdmin

from core.apps.main.models import AdModel, AdFilesModel, AdCountries
from django.contrib import admin


class AdCountriesInline(admin.TabularInline):
    model = AdCountries
    extra = 1


class AdFilesAdmin(admin.TabularInline):
    model = AdFilesModel
    extra = 1


@admin.register(AdModel)
class AdAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
    inlines = [AdFilesAdmin, AdCountriesInline]
