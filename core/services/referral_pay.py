from rest_framework.exceptions import ValidationError
from core.apps.referral.models import ReferralModel, ReferralHistoryModel, ReferralUsersModel
from core.apps.referral.choices.referral_history_choice import ReferralHistoryType
from core.apps.main.choices import PaymentsStatusChoice


def referral_payment_service(user, ad):
    if user.referral_amount < ad.total_price:
        raise ValidationError({"referral_amount": "Mablag' yetarli emas"})
    user.referral_amount -= ad.total_price
    user.save()
    ad.status = PaymentsStatusChoice.PAID
    ad.save()
    history = ReferralHistoryModel.objects.create(owner=user, ad=ad, amount=ad.total_price,
                                                  type=ReferralHistoryType.EXPENSE)
    history.save()
    return {'referral': "To'lov muvafaqiyatli amalga oshirildi!"}
