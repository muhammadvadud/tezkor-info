from rest_framework import serializers

from core.apps.main.models import AdModel, AdFilesModel, CategoryModel


class AdTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = [
            "id",
            "name",
        ]


class AdFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdFilesModel
        fields = [
            "id",
            "file"
        ]


class BaseMyadsSerializer(serializers.ModelSerializer):
    files = AdFilesSerializer(many=True, read_only=True)
    types = AdTypesSerializer(many=True, read_only=True)

    class Meta:
        model = AdModel
        fields = [
            "id",
            "title",
            "description",
            "total_view_count",
            "files",
            "status",
            "types",
        ]


class ListMyadsSerializer(BaseMyadsSerializer):
    class Meta(BaseMyadsSerializer.Meta): ...


class RetrieveMyadsSerializer(BaseMyadsSerializer):
    class Meta(BaseMyadsSerializer.Meta): ...


class CreateMyadsSerializer(BaseMyadsSerializer):
    class Meta(BaseMyadsSerializer.Meta):
        fields = [
            "id",
        ]
