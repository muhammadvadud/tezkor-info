from django_filters import rest_framework as filters

from core.apps.payments.models import CashbackModel


class CashbackFilter(filters.FilterSet):
    # name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = CashbackModel
        fields = [
            "name",
        ]
