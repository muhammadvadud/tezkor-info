import threading
import asyncio
from aiogram import Bot
from django.conf import settings
from .get_users import get_users_for_ad


def send_ad(ad):
    users = get_users_for_ad(ad)
    ad.sent_to.set(users)

    tg_ids = []
    for user in users:
        tg_ids.extend(user.user_tg_ids.values_list("tg_id", flat=True))

    tg_ids = list(set(tg_ids))
    count = len(tg_ids)
    ad.total_view_count = count
    ad.save()
    username = f"{ad.created_by.first_name} {ad.created_by.last_name}"
    ad_data = {
        "id": ad.id,
        "title": ad.title,
        "description": ad.description,
        "username": username,
        "phone": ad.phone_number,
    }

    files = [f.file.path for f in ad.files.all()]
    threading.Thread(
        target=_run_async_send, args=(ad_data, files, tg_ids)
    ).start()
    return True


def _run_async_send(ad_data, files, tg_ids):
    async def _task():
        bot = Bot(token=settings.BOT_TOKEN)
        from bot.utils.sender import send_ad_bot

        await send_ad_bot(ad_data, files, tg_ids, bot)
        await bot.session.close()

    asyncio.run(_task())
