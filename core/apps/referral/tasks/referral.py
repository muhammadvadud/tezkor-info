from ..models import ReferralModel, ReferralUsersModel


def user_add_for_referral(user):
    ref = ReferralModel.objects.filter(code=user.referral).first()
    if ref:
        ReferralUsersModel.objects.create(referral_owner=ref.user, referral_user=user)
        return True
    return False
