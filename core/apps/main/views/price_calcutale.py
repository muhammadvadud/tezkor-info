from rest_framework import viewsets, status
from rest_framework.response import Response
from ..serializers import PriceCalculationSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["PriceBracket"])
class PriceCalculationView(viewsets.GenericViewSet):
    serializer_class = PriceCalculationSerializer

    def list(self, request, *args, **kwargs):
        people_count = request.query_params.get("people_count")
        if people_count is None:
            return Response({"error": "people_count param is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            people_count = int(people_count)
        except ValueError:
            return Response({"error": "people_count must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={"people_count": people_count})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
