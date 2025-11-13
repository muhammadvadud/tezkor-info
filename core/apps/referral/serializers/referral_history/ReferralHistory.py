from rest_framework import serializers

from core.apps.referral.models import ReferralHistoryModel


class BaseReferralHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralHistoryModel
        fields = [
            "id",
            "amount",
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
