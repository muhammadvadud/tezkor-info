from django.contrib import admin
from unfold.admin import ModelAdmin

from core.apps.referral.models import ReferralHistoryModel


@admin.register(ReferralHistoryModel)
class ReferralHistoryAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
