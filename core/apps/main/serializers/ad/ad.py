from rest_framework import serializers
from django.contrib.auth import get_user_model

from core.apps.main.models import AdModel, AdFilesModel


class OwnerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "phone"]


class AdFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdFilesModel
        fields = [
            "file"
        ]


class BaseAdSerializer(serializers.ModelSerializer):
    creator = OwnerInfoSerializer(read_only=True)
    files = AdFilesSerializer(read_only=True, many=True)

    class Meta:
        model = AdModel
        fields = [
            "title",
            "description",
            "view_count",
            "creator",
            "files",
        ]


class ListAdSerializer(BaseAdSerializer):
    class Meta(BaseAdSerializer.Meta): ...


class RetrieveAdSerializer(BaseAdSerializer):
    class Meta(BaseAdSerializer.Meta): ...


class CreateAdSerializer(BaseAdSerializer):
    files = serializers.ListSerializer(child=serializers.FileField(), write_only=True, required=True)
    types = serializers.ListSerializer(child=serializers.CharField(), write_only=True, required=True)

    class Meta(BaseAdSerializer.Meta):
        fields = [
            "title",
            "description",
            "files",
            "types",
        ]

    def create(self, validated_data):
        user = self.context.get("request").user
        files = validated_data.pop("files", [])
        if files:
            raise serializers.ValidationError("Raise not found")
        validated_data["creator"] = user
        ad = AdModel.objects.create(**validated_data)
        for file in files:
            AdFilesModel.objects.create(ad=ad, files=files)
        return ad
