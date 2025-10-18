from django.db import models
from django.utils.translation import gettext_lazy as _


class RoleChoice(models.TextChoices):
    """
    User Role Choice
    """

    SUPERUSER = "superuser", _("Superuser")
    ADMIN = "admin", _("Admin")
    USER = "user", _("User")


class PersonTypeChoice(models.TextChoices):
    """
    Person Type Choice
    """

    INDIVIDUAL = "individual", _("Jismoniy shaxs")
    LEGAL_ENTITY = "legal_entity", _("Yuridik shaxs")
