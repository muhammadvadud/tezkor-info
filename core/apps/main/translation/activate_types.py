from modeltranslation.translator import TranslationOptions, register

from core.apps.main.models import ActivateTypesModel


@register(ActivateTypesModel)
class ActivateTypesTranslation(TranslationOptions):
    fields = []
