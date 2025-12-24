from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model

User = get_user_model()


class BusinessAboutFilter(filters.FilterSet):
    country = filters.CharFilter(
        field_name="district__region__country__name",
        lookup_expr="iexact"
    )

    region = filters.CharFilter(
        field_name="district__region__name",
        lookup_expr="iexact"
    )

    district = filters.CharFilter(
        field_name="district__name",
        lookup_expr="iexact"
    )

    types = filters.NumberFilter(
        field_name="activate_types__id",
        lookup_expr="exact"
    )

    class Meta:
        model = User
        fields = ["country", "region", "district", "types"]
