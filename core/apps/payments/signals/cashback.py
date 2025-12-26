from django.db.models.signals import post_save
from django.dispatch import receiver

from core.apps.payments.models import CashbackModel


@receiver(post_save, sender=CashbackModel)
def CashbackSignal(sender, instance, created, **kwargs): ...
