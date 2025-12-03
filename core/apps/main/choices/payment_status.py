from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentsStatusChoice(models.TextChoices):
    """
    Payments Status Choice
    """

    PENDING = "pending", _("Pending")
    PAID = "paid", _("Paid")
    VERIFIED = "verified", _("Verified")
    CANCELED = "canceled", _("Canceled")
