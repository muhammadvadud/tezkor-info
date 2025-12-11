from core.apps.main.models.ad import AdModel
from core.apps.main.choices.payment_status import PaymentsStatusChoice
from core.services.send_ad import send_ad
from django.db import transaction
from django.dispatch import receiver
from django.db.models.signals import pre_save


@receiver(pre_save, sender=AdModel)
def check_paid_status(sender, instance, **kwargs):
    if not instance.pk:
        return

    old = sender.objects.get(pk=instance.pk)
    if old.status != PaymentsStatusChoice.VERIFIED and instance.status == PaymentsStatusChoice.VERIFIED:
        transaction.on_commit(lambda: send_ad(instance))
