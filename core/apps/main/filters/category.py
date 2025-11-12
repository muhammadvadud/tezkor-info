from django_filters import rest_framework as filters

from core.apps.main.models import CategoryModel


class CategoryFilter(filters.FilterSet):
    class Meta:
        model = CategoryModel
        fields = [
            "name",
            "id",
            "code",
            "level",
            "is_leaf"
        ]
