import threading
import asyncio
from aiogram import Bot
from django.conf import settings
from core.apps.main.models import NotificationModel
from core.apps.accounts.models import UserTgIds


def send_notification(notification: NotificationModel):
    tg_ids = list(
        UserTgIds.objects.values_list("tg_id", flat=True).distinct()
    )

    files = [f.file.path for f in notification.files.all()]

    threading.Thread(
        target=_run_async_send,
        args=(notification, files, tg_ids)
    ).start()

    return True


def _run_async_send(notification, files, tg_ids):
    async def _task():
        bot = Bot(token=settings.BOT_TOKEN)
        from bot.utils.sender import send_user_notification

        await send_user_notification(notification, files, tg_ids, bot)

        await bot.session.close()

    asyncio.run(_task())
