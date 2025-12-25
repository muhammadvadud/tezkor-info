from core.apps.main.models import AdModel
from django.contrib.auth import get_user_model
from core.apps.referral.models import ReferralUsersModel
from core.apps.referral.models import ReferralHistoryModel
from core.apps.referral.choices import ReferralHistoryType


def payme_pay(ad):
    user = ad.created_by
    try:
        obj = ReferralUsersModel.objects.get(referral_user=user)
    except ReferralUsersModel.DoesNotExist:
        return False
    referral_owner = obj.referral_owner
    referral = obj.referral
    referral_share = referral.referral_share
    amount = (ad.total_price * referral_share) / 100
    referral_owner.referral_amount += amount
    referral_owner.save()
    referral.referral_posted_ads_count += 1
    referral.referral_income_amount += amount
    referral.save()
    ReferralHistoryModel.objects.create(amount=amount, referral=referral, ad=ad, owner=referral_owner,
                                        type=ReferralHistoryType.INCOME)

    return True
