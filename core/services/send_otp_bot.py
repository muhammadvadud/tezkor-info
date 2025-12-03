from django.utils.timezone import now


def get_or_return_sms_code(phone):
    from django_core.models.user import SmsConfirm
    try:
        sms_obj = SmsConfirm.objects.get(phone=phone)
    except SmsConfirm.DoesNotExist:
        return False
    if sms_obj.expire_time is None:
        return False
    if sms_obj.expire_time.timestamp() < now().timestamp():
        return False
    return sms_obj.code
