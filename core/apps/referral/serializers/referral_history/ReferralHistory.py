from rest_framework import serializers

from core.apps.referral.models import ReferralHistoryModel


class BaseReferralHistorySerializer(serializers.ModelSerializer):
    ad_title = serializers.CharField(
        source="ad.title",
        read_only=True
    )
    referral_code = serializers.CharField(
        source="referral.code",
        read_only=True
    )

    class Meta:
        model = ReferralHistoryModel
        fields = [
            "id",
            "amount",
            "type",
            "referral",
            "referral_code",
            "ad",
            "ad_title"
        ]


class ListReferralHistorySerializer(BaseReferralHistorySerializer):
    class Meta(BaseReferralHistorySerializer.Meta): ...


class RetrieveReferralHistorySerializer(BaseReferralHistorySerializer):
    class Meta(BaseReferralHistorySerializer.Meta): ...


class CreateReferralHistorySerializer(BaseReferralHistorySerializer):
    class Meta(BaseReferralHistorySerializer.Meta):
        fields = [
            "id",
            "amount",
        ]
