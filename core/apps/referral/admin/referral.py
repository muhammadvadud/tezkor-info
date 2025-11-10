from django.contrib import admin
from unfold.admin import ModelAdmin

from core.apps.referral.models import ReferralModel


@admin.register(ReferralModel)
class ReferralAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
