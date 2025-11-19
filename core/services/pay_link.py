import os
from core.apps.main.models import AdModel
from core.apps.main.choices import PaymentsStatusChoice
from rest_framework import serializers
from payme import Payme


def get_payme_url(ad_id, amount, return_url):
    payme_id = os.getenv('PAYME_ID')
    ad = AdModel.objects.get(id=ad_id)
    if ad.status != PaymentsStatusChoice.PENDING:
        raise serializers.ValidationError({"detail": "Ushbu ad uchun to‘lov allaqachon amalga oshirilgan."})

    payme = Payme(payme_id=payme_id)
    pay_link = payme.initializer.generate_pay_link(id=ad_id, amount=amount, return_url=return_url)
    return pay_link
