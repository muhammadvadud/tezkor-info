from rest_framework import serializers

from core.apps.main.models import AdModel, AdFilesModel, CategoryModel


class AdTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = [
            "id",
            "name",
            "icon_name",
        ]


class AdFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdFilesModel
        fields = [
            "id",
            "file"
        ]


class BaseDashboardAdsSerializer(serializers.ModelSerializer):
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


class ListDashboardAdsSerializer(BaseDashboardAdsSerializer):
    class Meta(BaseDashboardAdsSerializer.Meta): ...


class RetrieveDashboardAdsSerializer(BaseDashboardAdsSerializer):
    class Meta(BaseDashboardAdsSerializer.Meta): ...


class CreateDashboardAdsSerializer(BaseDashboardAdsSerializer):
    class Meta(BaseDashboardAdsSerializer.Meta):
        fields = [
            "id",
        ]
