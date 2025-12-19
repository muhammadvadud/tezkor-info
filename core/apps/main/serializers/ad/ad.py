from rest_framework import serializers
from django.contrib.auth import get_user_model

from core.apps.accounts.choices import PersonTypeChoice
from core.apps.main.choices import PaymentsTypeChoice
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


class AdFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdFilesModel
        fields = [
            "file"
        ]


class BaseAdSerializer(serializers.ModelSerializer):
    creator = OwnerInfoSerializer(read_only=True)
    files = AdFilesSerializer(read_only=True, many=True)
    company_selections = CompanySelectionModelSerializer(read_only=True, many=True)

    class Meta:
        model = AdModel
        fields = [
            "title",
            "description",
            "total_view_count",
            "creator",
            "files",
            "company_selections",
            "phone_number",
            "created_at",
        ]


class ListAdSerializer(BaseAdSerializer):
    class Meta(BaseAdSerializer.Meta): ...


class RetrieveAdSerializer(BaseAdSerializer):
    class Meta(BaseAdSerializer.Meta): ...


class CreateAdSerializer(BaseAdSerializer):
    files = serializers.ListSerializer(child=serializers.FileField(), write_only=True, required=True)
    types = serializers.ListSerializer(child=serializers.IntegerField(), write_only=True, required=True)
    company_selections = CompanySelectionModelSerializer(many=True, write_only=True)

    class Meta(BaseAdSerializer.Meta):
        fields = [
            "id",
            "title",
            "description",
            "files",
            "types",
            "total_price",
            "phone_number",
            "company_selections",
        ]
        extra_kwargs = {
            "total_price": {"required": True},
        }

    def create(self, validated_data):
        user = self.context.get("request").user
        files = validated_data.pop("files", [])
        types = validated_data.pop("types", [])
        company_selections = validated_data.pop("company_selections", [])
        if user.person_type == PersonTypeChoice.EMPLOYEE:
            user = user.parent
        validated_data["created_by"] = user
        ad = AdModel.objects.create(**validated_data)
        if files:
            for file in files:
                AdFilesModel.objects.create(ad=ad, file=file)
        if types:
            ad.types.set(types)
        if company_selections:
            ids_selections = []
            for company_selection in company_selections:
                selections = CompanySelectionModel.objects.create(**company_selection)
                ids_selections.append(selections.id)
            ad.company_selections.set(ids_selections)
            ad.save()
        return ad
