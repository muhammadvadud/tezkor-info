from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.apps.main.models import AdModel, AdFilesModel, CompanySelectionModel, CategoryModel


class OwnerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "phone"]


class CompanySelectionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanySelectionModel
        fields = [
            "id",
            "continent",
            "country",
            "region",
            "district",
            "letters",
            "total_companies",
            "ad_price",
            "total_price",
        ]


class ConfirmationAdsFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdFilesModel
        fields = [
            "file"
        ]


class BaseConfirmationAdsSerializer(serializers.ModelSerializer):
    creator = OwnerInfoSerializer(read_only=True)
    files = ConfirmationAdsFilesSerializer(read_only=True, many=True)
    company_selections = CompanySelectionModelSerializer(read_only=True, many=True)

    class Meta:
        model = AdModel
        fields = [
            "title",
            "description",
            "status",
            "total_view_count",
            "creator",
            "files",
            "company_selections",
            "phone_number",
        ]


class ListConfirmationAdsSerializer(BaseConfirmationAdsSerializer):
    class Meta(BaseConfirmationAdsSerializer.Meta): ...


class RetrieveConfirmationAdsSerializer(BaseConfirmationAdsSerializer):
    class Meta(BaseConfirmationAdsSerializer.Meta): ...


class UpdateConfirmationAdsSerializer(BaseConfirmationAdsSerializer):
    class Meta(BaseConfirmationAdsSerializer.Meta):
        fields = [
            "status",
        ]
