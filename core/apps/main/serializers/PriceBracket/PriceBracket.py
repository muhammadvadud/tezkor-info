from rest_framework import serializers

from core.apps.main.models import PriceBracketModel


class BasePricebracketSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceBracketModel
        fields = [
            "id",
            "name",
            "price_per_person",
        ]


class ListPricebracketSerializer(BasePricebracketSerializer):
    class Meta(BasePricebracketSerializer.Meta): ...


class RetrievePricebracketSerializer(BasePricebracketSerializer):
    class Meta(BasePricebracketSerializer.Meta): ...


class CreatePricebracketSerializer(BasePricebracketSerializer):
    class Meta(BasePricebracketSerializer.Meta):
        fields = [
            "id",
            "name",
        ]
