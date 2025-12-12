from rest_framework import serializers

from core.apps.main.models import ProductServiceModel, ProductServiceFilesModel
from django.contrib.auth import get_user_model
from core.apps.accounts.models.region import Country
from django.db.models import Count
from core.apps.main.models import CategoryModel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = [
            "name",
            "icon_name",
        ]


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
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = ProductServiceModel
        fields = [
            "id",
            "title",
            "description",
            "company",
            "files",
            "category",
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
    category = serializers.PrimaryKeyRelatedField(
        queryset=CategoryModel.objects.all(),
        many=True,
        write_only=True,
        required=True
    )

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
        categories = validated_data.pop("category", [])
        files = validated_data.pop("files", [])

        validated_data['company'] = self.context['request'].user

        product_service = ProductServiceModel.objects.create(**validated_data)

        product_service.category.set(categories)

        if files:
            for file in files:
                ProductServiceFilesModel.objects.create(
                    service=product_service,
                    file=file
                )
        product_service.save()
        return product_service

    def update(self, instance, validated_data):
        delete_files = validated_data.pop("delete_files", [])
        new_files = validated_data.pop("files", [])
        categories = validated_data.pop("category", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if categories is not None:
            instance.category.set(categories)

        if delete_files:
            instance.files.filter(id__in=delete_files).delete()

        if new_files:
            for f in new_files:
                ProductServiceFilesModel.objects.create(
                    service=instance,
                    file=f
                )

        return instance


class GetLegalEntitySerializer(serializers.ModelSerializer):
    product_service_company = BaseProductServiceSerializer(many=True, read_only=True)
    country_name = serializers.CharField(source="district.region.country.name", read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "company_name",
            "country_name",
            "product_service_company"
        ]


class GetCountrySerializer(serializers.ModelSerializer):
    companies = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = [
            "id",
            "name",
            "companies",
        ]

    def get_companies(self, obj):
        companies = (
            get_user_model().objects
            .filter(
                person_type="legal_entity",
                validated_at__isnull=False,
                district__region__country=obj
            )
            .annotate(service_count=Count("product_service_company"))
            .values("id", "company_name", "service_count")
            .distinct()
        )
        return companies
