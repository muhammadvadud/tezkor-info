from django_filters import rest_framework as filters

from core.apps.main.models import ProductServiceModel


class ProductServiceFilter(filters.FilterSet):
    # name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = ProductServiceModel
        fields = [
        ]
