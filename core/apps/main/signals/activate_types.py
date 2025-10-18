from core.apps.main.models import ActivateTypesModel
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=ActivateTypesModel)
def ActivateTypesSignal(sender, instance, created, **kwargs): ...
