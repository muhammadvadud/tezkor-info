from django.db import models
from django.utils.translation import gettext_lazy as _


class ReferralHistoryType(models.TextChoices):
    INCOME = "INCOME", _("Income")
    EXPENSE = "EXPENSE", _("Expense")
