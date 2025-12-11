from unfold.admin import ModelAdmin

from core.apps.main.models import AdModel, AdFilesModel
from django.contrib import admin


class AdFilesAdmin(admin.TabularInline):
    model = AdFilesModel
    extra = 1


@admin.register(AdModel)
class AdAdmin(ModelAdmin):
    list_display = (
        "id",
        "status",
        "title",
        "created_by",
        "total_view_count",
        "phone_number",
        "payments_type",

    )
    inlines = [AdFilesAdmin]
    autocomplete_fields = [
        "company_selections",
        "sent_to"
    ]
