from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from core.apps.payments.serializers.payments import PaymentsLinkSerializer
from rest_framework import status


@extend_schema(tags=["Payments"])
class PaymentsVIew(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, payment_type, ad_id):
        serializer = PaymentsLinkSerializer(
            data=request.data,
            context={"payment_type": payment_type, "ad_id": ad_id, "user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
