from django.contrib import admin
from unfold.admin import ModelAdmin

from core.apps.accounts.models import SignupBonusModel


@admin.register(SignupBonusModel)
class SignupBonusModelAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
