from django.contrib import admin
from unfold.admin import ModelAdmin

from core.apps.main.models import NotificationModel, NotificationFiles


class NotificationInlineAdmin(admin.TabularInline):
    model = NotificationFiles
    extra = 1


@admin.register(NotificationModel)
class NotificationAdmin(ModelAdmin):
    list_display = (
        "id",
        "__str__",
    )
    inlines = [NotificationInlineAdmin]
