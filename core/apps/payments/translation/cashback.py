from modeltranslation.translator import TranslationOptions, register

from core.apps.payments.models import CashbackModel


@register(CashbackModel)
class CashbackTranslation(TranslationOptions):
    fields = []
