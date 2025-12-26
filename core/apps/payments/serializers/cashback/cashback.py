from rest_framework import serializers
from core.apps.payments.models import CashbackModel
from core.apps.main.models import AdModel


class CashbackAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdModel
        fields = [
            "title",
            "description",
        ]


class BaseCashbackSerializer(serializers.ModelSerializer):
    ad = CashbackAdSerializer(read_only=True)

    class Meta:
        model = CashbackModel
        fields = [
            "id",
            "ad",
            "amount",
            "percent",
            "created_at",
        ]


class ListCashbackSerializer(BaseCashbackSerializer):
    class Meta(BaseCashbackSerializer.Meta): ...


class RetrieveCashbackSerializer(BaseCashbackSerializer):
    class Meta(BaseCashbackSerializer.Meta): ...


class CreateCashbackSerializer(BaseCashbackSerializer):
    class Meta(BaseCashbackSerializer.Meta):
        fields = [
            "id",
            "name",
        ]
