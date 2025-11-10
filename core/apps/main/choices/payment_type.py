from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentsTypeChoice(models.TextChoices):
    """
    Payments Type Choice
    """

    CLICK = "CLICK", _("Click")
    PAYME = "PAYME", _("Payme")
    OTHER = "OTHER", _("Other")
