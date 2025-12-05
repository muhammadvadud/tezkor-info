from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.apps.main.models.product_service import ProductServiceModel, ProductServiceFilesModel
from core.apps.accounts.models import CategoryModel


class ProductServiceFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductServiceFilesModel
        fields = [
            "file"
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = [
            "id",
            "name",
            "icon_name",
        ]


class ProductServiceCompanySerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    files = ProductServiceFilesSerializer(many=True, read_only=True)

    class Meta:
        model = ProductServiceModel
        fields = [
            "title",
            "description",
            "title",
            "category",
            "files"
        ]


class BaseBusinessAboutSerializer(serializers.ModelSerializer):
    product_service_company = ProductServiceCompanySerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "company_name",
            "director_full_name",
            "company_image",
            "phone",
            "product_service_company",
        ]


class ListBusinessAboutSerializer(BaseBusinessAboutSerializer):
    class Meta(BaseBusinessAboutSerializer.Meta):
        fields = [
            "id",
            "company_name"
        ]


class RetrieveBusinessAboutSerializer(BaseBusinessAboutSerializer):
    class Meta(BaseBusinessAboutSerializer.Meta): ...


class CreateBusinessAboutSerializer(BaseBusinessAboutSerializer):
    class Meta(BaseBusinessAboutSerializer.Meta):
        fields = [
            "id",
        ]
