from rest_framework import serializers

from core.apps.main.models import ActivateTypesModel


class BaseActivateTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivateTypesModel
        fields = [
            "id",
            "name",
            "image",
        ]


class ListActivateTypesSerializer(BaseActivateTypesSerializer):
    class Meta(BaseActivateTypesSerializer.Meta): ...


class RetrieveActivateTypesSerializer(BaseActivateTypesSerializer):
    class Meta(BaseActivateTypesSerializer.Meta): ...


class CreateActivateTypesSerializer(BaseActivateTypesSerializer):
    class Meta(BaseActivateTypesSerializer.Meta):
        fields = [
            "id",
            "name",
        ]
