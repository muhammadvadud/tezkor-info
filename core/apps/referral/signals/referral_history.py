from django.db.models.signals import post_save
from django.dispatch import receiver

from core.apps.referral.models import ReferralHistoryModel


@receiver(post_save, sender=ReferralHistoryModel)
def ReferralHistorySignal(sender, instance, created, **kwargs): ...
