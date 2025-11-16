from django.db.models.signals import post_save
from django.dispatch import receiver

from core.apps.main.models import ProductServiceModel


@receiver(post_save, sender=ProductServiceModel)
def ProductServiceSignal(sender, instance, created, **kwargs): ...
