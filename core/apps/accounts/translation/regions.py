from modeltranslation.translator import TranslationOptions, register

from core.apps.accounts.models import Country, Region, District


@register(Country)
class CountryTranslation(TranslationOptions):
    fields = [
        "name",
    ]


@register(Region)
class RegionTranslation(TranslationOptions):
    fields = [
        "name",
    ]


@register(District)
class DistrictTranslation(TranslationOptions):
    fields = [
        "name",
    ]
