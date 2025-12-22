from django.utils.timezone import now
import asyncio
from aiogram import Bot
from django.conf import settings
from django.contrib.auth import get_user_model
import threading
from django.utils.timezone import now


def get_or_return_sms_code(phone):
    from django_core.models.user import SmsConfirm

    try:
        sms_obj = SmsConfirm.objects.get(phone=phone)
    except SmsConfirm.DoesNotExist:
        return False, "SMS_NOT_FOUND"

    if sms_obj.expire_time is None:
        return False, "EXPIRE_TIME_IS_NONE"

    if sms_obj.expire_time < now():
        return False, "SMS_EXPIRED"

    return sms_obj.code


def send_code_for_bot(phone, code):
    user = get_user_model().objects.get(phone=phone)
    tg_ids = []
    if user.user_tg_ids is not None:
        for tg in user.user_tg_ids.all():
            tg_ids.append(tg.tg_id)
        threading.Thread(
            target=_run_async_send, args=(tg_ids, code)
        ).start()

        return True
    return


def _run_async_send(tg_ids, code):
    async def _task():
        bot = Bot(token=settings.BOT_TOKEN)
        from bot.handlers.send_code_login import send_otp_to_users

        await send_otp_to_users(bot, tg_ids, code)
        await bot.session.close()

    asyncio.run(_task())
