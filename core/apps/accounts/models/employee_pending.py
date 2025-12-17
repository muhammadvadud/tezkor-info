from django.db import models
from django_core.models.base import AbstractBaseModel
from django.utils.translation import gettext_lazy as _


class EmployeePendingModel(AbstractBaseModel):
    full_name = models.CharField(_("Full Name"), max_length=255)
    phone_number = models.CharField(_("Phone Number"), max_length=255)
    stir = models.CharField(_("Stir"), max_length=255)
    tg_id = models.CharField(_("TG ID"), max_length=255, null=True, blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "employee_pending"
        verbose_name = "Employee Pending"
        verbose_name_plural = "Employee Pending"
