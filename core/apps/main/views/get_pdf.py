from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions, mixins
from core.apps.main.models import AdModel
from core.apps.main.serializers import GetPDFSerializer
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["ad"])
class GetPdfViewSet(viewsets.ModelViewSet):
    queryset = AdModel.objects.all()
    serializer_class = GetPDFSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["post"]

    @action(detail=False, methods=["post"])
    def generate_pdf(self, request):
        ad_id = request.data.get("ad_id")

        if not ad_id:
            return Response(
                {"ad_id": "ad_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        ad = get_object_or_404(AdModel, id=ad_id)

        serializer = GetPDFSerializer(ad)
        return Response(serializer.data, status=status.HTTP_200_OK)
