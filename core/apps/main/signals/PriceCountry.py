from django.db.models.signals import post_save
from django.dispatch import receiver

from core.apps.main.models import PriceCountryModel


@receiver(post_save, sender=PriceCountryModel)
def PriceCountrySignal(sender, instance, created, **kwargs): ...
