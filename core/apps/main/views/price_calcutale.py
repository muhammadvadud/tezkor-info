from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.apps.accounts.models import User
from core.apps.accounts.models.region import Country, Region, District
from core.apps.main.models import PriceCountryModel
from core.apps.main.serializers import PriceCalculateSerializer
from core.apps.accounts.choices.user import PersonTypeChoice
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["price-calculate"])
class PriceCalculationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = PriceCalculateSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        country_name = serializer.validated_data["country"]
        region_name = serializer.validated_data["region"]
        district_name = serializer.validated_data["district"]
        letters = serializer.validated_data["letters"]

        # 1️⃣ Country
        try:
            country = Country.objects.get(name__iexact=country_name)
        except Country.DoesNotExist:
            return Response({"error": "Country not found"}, status=400)

        # 2️⃣ Region (all or exact)
        if region_name.lower() == "all":
            regions = Region.objects.filter(country=country)
        else:
            try:
                region = Region.objects.get(name__iexact=region_name, country=country)
                regions = [region]
            except Region.DoesNotExist:
                return Response({"error": "Region not found"}, status=400)

        # 3️⃣ District (all or exact)
        if district_name.lower() == "all":
            districts = District.objects.filter(region__in=regions)
        else:
            try:
                district = District.objects.get(name__iexact=district_name, region__in=regions)
                districts = [district]
            except District.DoesNotExist:
                return Response({"error": "District not found"}, status=400)

        # 4️⃣ User filter
        users = User.objects.filter(
            person_type=PersonTypeChoice.LEGAL_ENTITY,
            district__in=districts,
            company_name__istartswith=letters
        )

        user_count = users.count()

        # 5️⃣ Price
        try:
            country_price = PriceCountryModel.objects.get(country=country).price
        except PriceCountryModel.DoesNotExist:
            return Response({"error": "Price for this country not found"}, status=400)

        # 6️⃣ Total
        total_price = user_count * country_price

        return Response({
            "country": country.name,
            "region": region_name,
            "district": district_name,
            "letters": letters,
            "country_price": country_price,
            "user_count": user_count,
            "total_price": total_price
        })
