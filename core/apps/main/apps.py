from django.apps import AppConfig


class ModuleConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core.apps.main"

    def ready(self):
        import core.apps.main.signals