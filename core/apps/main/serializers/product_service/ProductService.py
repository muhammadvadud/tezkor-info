from rest_framework import serializers

from core.apps.main.models import ProductServiceModel


class BaseProductServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductServiceModel
        fields = [
            "id",
            "name",
        ]


class ListProductServiceSerializer(BaseProductServiceSerializer):
    class Meta(BaseProductServiceSerializer.Meta): ...


class RetrieveProductServiceSerializer(BaseProductServiceSerializer):
    class Meta(BaseProductServiceSerializer.Meta): ...


class CreateProductServiceSerializer(BaseProductServiceSerializer):
    class Meta(BaseProductServiceSerializer.Meta):
        fields = [
            "id",
            "name",
        ]
