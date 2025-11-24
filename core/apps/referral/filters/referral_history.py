from django_filters import rest_framework as filters

from core.apps.referral.models import ReferralHistoryModel


class ReferralHistoryFilter(filters.FilterSet):
    class Meta:
        model = ReferralHistoryModel
        fields = [
            "type",
        ]
