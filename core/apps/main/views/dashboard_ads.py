from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from core.apps.accounts.choices.user import PersonTypeChoice
from core.apps.main.models import AdModel
from core.apps.main.choices import PaymentsStatusChoice
from core.apps.main.serializers.dashboard_ads import (
    CreateDashboardAdsSerializer,
    ListDashboardAdsSerializer,
    RetrieveDashboardAdsSerializer,
)


@extend_schema(tags=["DashboardAds"])
class DashboardAdsView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = AdModel.objects.all()
    serializer_class = ListDashboardAdsSerializer
    permission_classes = [AllowAny]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListDashboardAdsSerializer,
        "retrieve": RetrieveDashboardAdsSerializer,
        "create": CreateDashboardAdsSerializer,
    }

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return AdModel.objects.all().order_by("-id")

        if user.person_type == PersonTypeChoice.LEGAL_ENTITY:
            return (
                AdModel.objects
                .filter(types__in=user.activate_types.all(), status=PaymentsStatusChoice.VERIFIED)
                .distinct()
                .order_by("-id")
            )

        if (
                user.person_type == PersonTypeChoice.EMPLOYEE
                and user.parent
        ):
            return (
                AdModel.objects
                .filter(types__in=user.parent.activate_types.all(), status=PaymentsStatusChoice.VERIFIED)
                .distinct()
                .order_by("-id")
            )

        return AdModel.objects.none()
