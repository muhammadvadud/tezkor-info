from django.dispatch import receiver
from django.db.models.signals import pre_save

from core.apps.main.models import NotificationModel
from core.services.send_user_notification import send_notification


@receiver(pre_save, sender=NotificationModel)
def NotificationSignal(sender, instance, **kwargs):
    if not instance.pk:
        return
    if instance.is_send is True:
        return send_notification(instance)
    return
