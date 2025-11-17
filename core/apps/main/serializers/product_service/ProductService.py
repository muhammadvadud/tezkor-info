from rest_framework import serializers

from core.apps.main.models import ProductServiceModel, ProductServiceFilesModel
from django.contrib.auth import get_user_model


class CompanyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "company_name",
        ]


class ProductServiceFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductServiceFilesModel
        fields = [
            "id",
            "file"
        ]


class BaseProductServiceSerializer(serializers.ModelSerializer):
    files = ProductServiceFilesSerializer(many=True, read_only=True)
    company = serializers.CharField(source="company.company_name", read_only=True)

    class Meta:
        model = ProductServiceModel
        fields = [
            "id",
            "title",
            "description",
            "company",
            "files",
        ]


class ListProductServiceSerializer(BaseProductServiceSerializer):
    class Meta(BaseProductServiceSerializer.Meta): ...


class RetrieveProductServiceSerializer(BaseProductServiceSerializer):
    class Meta(BaseProductServiceSerializer.Meta): ...


class CreateProductServiceSerializer(BaseProductServiceSerializer):
    files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True
    )
    delete_files = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)

    class Meta(BaseProductServiceSerializer.Meta):
        fields = [
            "id",
            "title",
            "description",
            "category",
            "files",
            "delete_files",
        ]

    def create(self, validated_data):
        files = validated_data.pop("files", [])
        validated_data['company'] = self.context['request'].user
        product_service = ProductServiceModel.objects.create(**validated_data)
        if files:
            for file in files:
                ProductServiceFilesModel.objects.create(service=product_service, file=file)
        return product_service

    def update(self, instance, validated_data):
        delete_files = validated_data.pop("delete_files", [])
        print(delete_files)
        new_files = validated_data.pop("files", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if delete_files:
            instance.files.filter(id__in=delete_files).delete()

        if new_files:
            for f in new_files:
                ProductServiceFilesModel.objects.create(
                    service=instance,
                    file=f
                )

        return instance
