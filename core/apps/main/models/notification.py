from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from model_bakery import baker


class NotificationModel(AbstractBaseModel):
    title = models.CharField(verbose_name=_("name"), max_length=255)
    description = models.TextField(verbose_name=_("description"))
    is_send = models.BooleanField(verbose_name=_("is send"), default=False)

    def __str__(self):
        return str(self.pk)

    @classmethod
    def _baker(cls):
        return baker.make(cls)

    class Meta:
        db_table = "notification"
        verbose_name = _("NotificationModel")
        verbose_name_plural = _("NotificationModels")


class NotificationFiles(AbstractBaseModel):
    file = models.FileField(verbose_name=_("Notification Files"), upload_to="notification_files/")
    notification = models.ForeignKey(NotificationModel, on_delete=models.CASCADE, verbose_name=_("notification"),
                                     related_name="files")

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = "notification_files"
        verbose_name = _("NotificationFiles")
        verbose_name_plural = _("NotificationFiles")
