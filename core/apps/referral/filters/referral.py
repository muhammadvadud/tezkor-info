from django_filters import rest_framework as filters

from core.apps.referral.models import ReferralModel


class ReferralFilter(filters.FilterSet):
    # name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = ReferralModel
        fields = [
        ]
