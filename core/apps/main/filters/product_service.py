from django_filters import rest_framework as filters

from core.apps.main.models import ProductServiceModel


class ProductServiceFilter(filters.FilterSet):
    # name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    my = filters.BooleanFilter(method="filter_my")

    class Meta:
        model = ProductServiceModel
        fields = []

    def filter_my(self, queryset, name, value):
        if value:
            return queryset.filter(company=self.request.user)
        return queryset
