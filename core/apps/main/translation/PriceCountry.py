from modeltranslation.translator import TranslationOptions, register

from core.apps.main.models import PriceCountryModel


@register(PriceCountryModel)
class PriceCountryTranslation(TranslationOptions):
    fields = []
