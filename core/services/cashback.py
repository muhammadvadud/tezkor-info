from core.apps.payments.models import CashbackPercentModel, CashbackModel


def give_cashback(ad):
    percent_obj = CashbackPercentModel.objects.first()
    if not percent_obj:
        return False
    user = ad.created_by
    price = ad.total_price
    percent = percent_obj.percent
    cashback_amount = (price * percent) / 100
    user.referral_amount += cashback_amount
    user.save()
    CashbackModel.objects.create(ad=ad, user=user, amount=cashback_amount, percent=percent)
    return True
