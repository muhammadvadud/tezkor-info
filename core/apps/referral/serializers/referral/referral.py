from rest_framework import serializers

from core.apps.referral.models import ReferralModel


class BaseReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralModel
        fields = [
            "id",
            "code",
            "user",
            "referral_registered_count",
            "referral_posted_ads_count",
            "referral_income_amount",
        ]


class ListReferralSerializer(BaseReferralSerializer):
    class Meta(BaseReferralSerializer.Meta): ...


class RetrieveReferralSerializer(BaseReferralSerializer):
    class Meta(BaseReferralSerializer.Meta): ...


class CreateReferralSerializer(BaseReferralSerializer):
    class Meta(BaseReferralSerializer.Meta):
        fields = [
            "id",
            "code",
            "user",
            "referral_registered_count",
            "referral_posted_ads_count",
            "referral_income_amount",
        ]
