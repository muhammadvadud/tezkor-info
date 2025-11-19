from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from core.apps.main.models import AdModel
from django.shortcuts import get_object_or_404
from core.services.pay_link import get_payme_url


class PaymentsLinkSerializer(serializers.Serializer):
    return_url = serializers.CharField(write_only=True, required=True)
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        payment_type = self.context.get("payment_type")
        ad_id = self.context.get("ad_id")
        return_url = obj.get("return_url")

        if not payment_type:
            raise ValidationError("Payment type is required")

        if not return_url:
            raise serializers.ValidationError({"return_url": "Return URL is required."})

        ad = get_object_or_404(AdModel, pk=ad_id)
        amount = ad.total_price
        if payment_type == "payme":
            return get_payme_url(
                ad_id=ad_id,
                amount=amount,
                return_url=return_url,
            )
        elif payment_type == "referral":
            user = self.context.get("user")
            if user.referral_amount < amount:
                raise serializers.ValidationError({"referral_amount": "Not enough money"})
            return "zo'r"
        else:
            raise ValidationError("Payment type is invalid")
