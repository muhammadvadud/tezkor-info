from unfold.admin import ModelAdmin

from core.apps.accounts.models.region import Region, District, Country
from django.contrib import admin


@admin.register(Region)
class RegionAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )


@admin.register(District)
class DistrictAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )


@admin.register(Country)
class CountryAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
