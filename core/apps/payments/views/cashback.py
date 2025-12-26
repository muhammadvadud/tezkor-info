from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.apps.payments.models import CashbackModel
from core.apps.payments.serializers.cashback import (
    CreateCashbackSerializer,
    ListCashbackSerializer,
    RetrieveCashbackSerializer,
)


@extend_schema(tags=["cashback"])
class CashbackView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = CashbackModel.objects.all()
    serializer_class = ListCashbackSerializer
    permission_classes = [IsAuthenticated]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListCashbackSerializer,
        "retrieve": RetrieveCashbackSerializer,
        "create": CreateCashbackSerializer,
    }

    def get_queryset(self):
        return CashbackModel.objects.filter(user=self.request.user)
