from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    OpenApiTypes,
)
from ..serializers import CompanyLetterSummarySerializer


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="letters",
            description="Vergul bilan ajratilgan harflar, masalan: A,B,C",
            required=True,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            examples=[
                OpenApiExample(
                    "Misol",
                    value="A,B,C",
                    summary="Bir nechta harf bilan filter"
                )
            ],
        ),
    ],
    tags=["ad"],
    responses=CompanyLetterSummarySerializer,
)
class CompanyLetterSummaryView(viewsets.GenericViewSet):
    serializer_class = CompanyLetterSummarySerializer

    def list(self, request, *args, **kwargs):
        letters_param = request.query_params.get('letters', '')
        if not letters_param:
            return Response(
                {"error": "letters param is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data={"letters": letters_param})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
