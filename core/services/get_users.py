from django.contrib.auth import get_user_model
from django.db.models import Q
from core.apps.accounts.choices import PersonTypeChoice
from core.apps.accounts.models import Country, Region, District

User = get_user_model()


def get_users_for_ad(ad):
    selections = ad.company_selections.all()
    types = list(ad.types.all())
    user_ids = set()

    for s in selections:
        q = Q(person_type=PersonTypeChoice.LEGAL_ENTITY)

        try:
            country = Country.objects.get(name__iexact=s.country)
        except Country.DoesNotExist:
            continue

        if s.region.lower() == "all":
            regions = Region.objects.filter(country=country)
        else:
            try:
                regions = [Region.objects.get(name__iexact=s.region, country=country)]
            except Region.DoesNotExist:
                continue

        if s.district.lower() == "all":
            districts = District.objects.filter(region__in=regions)
        else:
            try:
                districts = [District.objects.get(name__iexact=s.district, region__in=regions)]
            except District.DoesNotExist:
                continue

        letter_filter = Q()
        if s.letters.lower() != "all":
            letters_list = [x.strip().upper() for x in s.letters.split(",")]
            for letter in letters_list:
                letter_filter |= Q(company_name__istartswith=letter)

        limit = s.total_companies

        qs = User.objects.filter(
            q,
            district__in=districts,
            activate_types__in=types
        )

        if letter_filter:
            qs = qs.filter(letter_filter)

        qs = qs.distinct()[:limit].values_list("id", flat=True)

        user_ids.update(list(qs))

    return User.objects.filter(id__in=user_ids)
