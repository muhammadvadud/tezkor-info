from rest_framework import serializers

from core.apps.main.models import CategoryModel


class ListCategoryTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = CategoryModel
        fields = [
            'id',
            'name',
            'code',
            'level',
            'is_leaf',
            'children',
            'icon_name'

        ]

    def get_children(self, obj):
        qs = obj.children.all()
        if obj.is_leaf:
            return []
        return ListCategoryTreeSerializer(qs, many=True, context=self.context).data


class BaseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = [
            'id',
            'name',
            'code',
            'level',
            'is_leaf',
            'icon_name',
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
