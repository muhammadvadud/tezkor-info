from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.apps.accounts.models import User
from core.apps.accounts.models.region import Country, Region, District
from core.apps.main.models import PriceCountryModel
from core.apps.main.serializers import PriceCalculateSerializer
from core.apps.accounts.choices.user import PersonTypeChoice
from drf_spectacular.utils import extend_schema
from django.db.models import Q


@extend_schema(tags=["price-calculate"])
class PriceCalculationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = PriceCalculateSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        country_name = serializer.validated_data["country"]
        region_name = serializer.validated_data["region"]
        district_name = serializer.validated_data["district"]
        letters_raw = serializer.validated_data["letters"]

        # 1) Letters → list
        letters = [l.strip() for l in letters_raw.split(",") if l.strip()]

        # 2) Country
        try:
            country = Country.objects.get(name__iexact=country_name)
        except Country.DoesNotExist:
            return Response({"error": "Country not found"}, status=400)

        # 3) Region
        if region_name.lower() == "all":
            regions = Region.objects.filter(country=country)
        else:
            try:
                region = Region.objects.get(name__iexact=region_name, country=country)
                regions = [region]
            except Region.DoesNotExist:
                return Response({"error": "Region not found"}, status=400)

        # 4) District
        if district_name.lower() == "all":
            districts = District.objects.filter(region__in=regions)
        else:
            try:
                district = District.objects.get(name__iexact=district_name, region__in=regions)
                districts = [district]
            except District.DoesNotExist:
                return Response({"error": "District not found"}, status=400)

        # 5) Create OR filter for letters
        q_filter = Q()
        for l in letters:
            q_filter |= Q(company_name__istartswith=l)

        # 6) Users
        users = User.objects.filter(
            person_type=PersonTypeChoice.LEGAL_ENTITY,
            district__in=districts
        ).filter(q_filter)

        user_count = users.count()

        # 7) Country price
        try:
            country_price = PriceCountryModel.objects.get(country=country).price
        except PriceCountryModel.DoesNotExist:
            return Response({"error": "Price for this country not found"}, status=400)

        # 8) Total
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
