from core.apps.main.models import AdModel
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=AdModel)
def AdSignal(sender, instance, created, **kwargs): ...
