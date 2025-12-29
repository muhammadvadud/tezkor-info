from rest_framework import serializers

from core.apps.accounts.models import Country, Region, District


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = [
            'id',
            'name',
            "code",
        ]


class RegionSerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(many=True, read_only=True)

    class Meta:
        model = Region
        fields = [
            "id",
            "name",
            "code",
            "districts",

        ]


class BaseCountriesSerializer(serializers.ModelSerializer):
    region = RegionSerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = [
            'id',
            'name',
            'region',
            'code',
        ]


class ListCountriesSerializer(BaseCountriesSerializer):
    class Meta(BaseCountriesSerializer.Meta): ...


class RetrieveCountriesSerializer(BaseCountriesSerializer):
    class Meta(BaseCountriesSerializer.Meta): ...


class CreateCountriesSerializer(BaseCountriesSerializer):
    class Meta(BaseCountriesSerializer.Meta):
        fields = [
            "id",
            "name",
        ]
