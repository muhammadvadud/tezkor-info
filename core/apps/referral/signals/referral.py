from django.db.models.signals import post_save
from django.dispatch import receiver

from core.apps.referral.models import ReferralModel


@receiver(post_save, sender=ReferralModel)
def ReferralSignal(sender, instance, created, **kwargs): ...
