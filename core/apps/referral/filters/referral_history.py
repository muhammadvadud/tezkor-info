from django_filters import rest_framework as filters

from core.apps.referral.models import ReferralHistoryModel


class ReferralHistoryFilter(filters.FilterSet):
    # name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = ReferralHistoryModel
        fields = [
            "name",
        ]
