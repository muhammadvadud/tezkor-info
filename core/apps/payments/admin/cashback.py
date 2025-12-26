from django.contrib import admin
from unfold.admin import ModelAdmin

from core.apps.payments.models import CashbackModel, CashbackPercentModel


@admin.register(CashbackModel)
class CashbackAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )


@admin.register(CashbackPercentModel)
class CashbackPercentAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
