from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.apps.accounts.models import User
from core.apps.accounts.models.region import Country, Region, District
from core.apps.main.models import PriceCountryModel, PriceBracket
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
        types = serializer.validated_data["types"]

        letters = [l.strip() for l in letters_raw.split(",") if l.strip()]
        types = [l.strip() for l in types.split(",") if l.strip()]

        try:
            country = Country.objects.get(code=country_name)
        except Country.DoesNotExist:
            return Response({"error": "Country not found"}, status=400)

        if region_name.lower() == "all":
            regions = Region.objects.filter(country=country)
        else:
            try:
                region = Region.objects.get(name__iexact=region_name, country=country)
                regions = [region]
            except Region.DoesNotExist:
                return Response({"error": "Region not found"}, status=400)

        if district_name.lower() == "all":
            districts = District.objects.filter(region__in=regions)
        else:
            try:
                district = District.objects.get(name__iexact=district_name, region__in=regions)
                districts = [district]
            except District.DoesNotExist:
                return Response({"error": "District not found"}, status=400)

        q_filter = Q()
        for l in letters:
            q_filter |= Q(company_name__istartswith=l)

        users = User.objects.filter(
            person_type=PersonTypeChoice.LEGAL_ENTITY,
            district__in=districts,
            activate_types__in=types,
        ).filter(q_filter)

        user_count = users.count()

        try:
            bracket = PriceBracket.objects.get(
                min_person__lte=user_count,
                max_person__gte=user_count
            )
            price_per_person = bracket.price
        except PriceBracket.DoesNotExist:
            return Response({"error": "No price bracket found for this user count"}, status=400)

        total_price = user_count * price_per_person
        user_ids = list(users.values_list("id", flat=True))

        return Response({
            "country": country.name,
            "region": region_name,
            "district": district_name,
            "letters": letters,
            "one_person_price": price_per_person,
            "user_count": user_count,
            "total_price": total_price,
            "user_ids": user_ids
        })
