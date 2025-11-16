from modeltranslation.translator import TranslationOptions, register

from core.apps.main.models import ProductServiceModel


@register(ProductServiceModel)
class ProductServiceTranslation(TranslationOptions):
    fields = []
