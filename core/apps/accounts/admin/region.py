from unfold.admin import ModelAdmin

from core.apps.accounts.models.region import Region, District, Country
from django.contrib import admin
from core.apps.accounts.models import UserTgIds


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


@admin.register(UserTgIds)
class UserTgIdsAdmin(ModelAdmin):
    search_fields = ["id"]
    list_display = (
        "id",
        "__str__",
    )
