from modeltranslation.translator import TranslationOptions, register

from core.apps.main.models import CategoryModel


@register(CategoryModel)
class CategoryTranslation(TranslationOptions):
    fields = [
        "name",
    ]
