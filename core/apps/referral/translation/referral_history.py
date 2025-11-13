from modeltranslation.translator import TranslationOptions, register

from core.apps.referral.models import ReferralHistoryModel


@register(ReferralHistoryModel)
class ReferralHistoryTranslation(TranslationOptions):
    fields = []
