from modeltranslation.translator import TranslationOptions, register

from core.apps.main.models import AdModel


@register(AdModel)
class AdTranslation(TranslationOptions):
    fields = []
