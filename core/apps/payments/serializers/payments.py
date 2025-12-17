from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.apps.accounts.choices import PersonTypeChoice
from core.apps.main.models import AdModel
from django.shortcuts import get_object_or_404
from core.services.pay_link import get_payme_url
from core.apps.main.choices import PaymentsStatusChoice
from core.services.referral_pay import referral_payment_service


class PaymentsLinkSerializer(serializers.Serializer):
    return_url = serializers.CharField(write_only=True, required=True)
    url = serializers.SerializerMethodField()

    def validate(self, attrs):
        user = self.context.get("user")
        ad_id = self.context.get("ad_id")
        if user.person_type == PersonTypeChoice.EMPLOYEE:
            user = user.parent

        try:
            ad = AdModel.objects.get(id=ad_id)
        except AdModel.DoesNotExist:
            raise serializers.ValidationError("Bunday reklama mavjud emas.")

        if ad.created_by != user:
            raise serializers.ValidationError({"ads": "Siz ushbu reklama uchun to'lov qila olmaysiz."})

        attrs["ad"] = ad
        return attrs

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
            if ad.status != PaymentsStatusChoice.PENDING:
                raise ValidationError({"ad": "To'lov amalga oshirilgan!"})
            user = self.context.get("user")
            if user.person_type == PersonTypeChoice.EMPLOYEE:
                user = user.parent
            pay_referral = referral_payment_service(user, ad)

            return pay_referral
        else:
            raise ValidationError("Payment type is invalid")
