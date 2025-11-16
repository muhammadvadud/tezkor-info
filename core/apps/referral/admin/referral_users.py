from django.contrib import admin
from unfold.admin import ModelAdmin

from core.apps.referral.models import ReferralUsersModel


@admin.register(ReferralUsersModel)
class ReferralUsersAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
