from rest_framework import serializers

from core.apps.main.models import CategoryModel


class BaseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = [
            'id',
            'name',
            'code',
            'level',
            'is_leaf',
        ]


class ListCategorySerializer(BaseCategorySerializer):
    class Meta(BaseCategorySerializer.Meta): ...


class RetrieveCategorySerializer(BaseCategorySerializer):
    class Meta(BaseCategorySerializer.Meta): ...


class CreateCategorySerializer(BaseCategorySerializer):
    class Meta(BaseCategorySerializer.Meta):
        fields = [
            "id",
            "name",
        ]
