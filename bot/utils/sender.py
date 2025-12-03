from aiogram.types import FSInputFile, InputMediaPhoto, InputMediaVideo, InputMediaDocument
from bot.main import Bot
import os


async def send_ad_bot(ad_data, files, tg_ids, bot: Bot):
    caption = f"""
🆕 Yangi reklama!

📌 <b>{ad_data['title']}</b>

{ad_data['description']}
{ad_data['username']}
{ad_data['phone']}
"""

    if not files:
        for tg_id in tg_ids:
            try:
                await bot.send_message(tg_id, caption, parse_mode="HTML")
            except Exception as e:
                print(f"[ERROR] Matn yuborilmadi ({tg_id}): {e}")
        return

    media_group = []

    for index, file_path in enumerate(files):
        ext = os.path.splitext(file_path)[1].lower()
        input_file = FSInputFile(file_path)

        if ext in [".jpg", ".jpeg", ".png", ".webp"]:
            media = InputMediaPhoto(media=input_file)
        elif ext in [".mp4", ".mov", ".avi"]:
            media = InputMediaVideo(media=input_file)
        else:
            media = InputMediaPhoto(media=input_file)

        if index == 0:
            media.caption = caption
            media.parse_mode = "HTML"

        media_group.append(media)

    for tg_id in tg_ids:
        try:
            await bot.send_media_group(chat_id=tg_id, media=media_group)
        except Exception as e:
            print(f"[ERROR] Media-group yuborilmadi ({tg_id}): {e}")


async def send_user_notification(notification, files, tg_ids, bot):
    caption = f"📢 *{notification.title}*\n\n{notification.description}"

    media_group = []

    for idx, file_path in enumerate(files):
        ext = os.path.splitext(file_path)[1].lower()
        file_obj = FSInputFile(file_path)

        if ext in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]:
            media = InputMediaPhoto(
                media=file_obj,
                caption=caption if idx == 0 else None,
                parse_mode="Markdown"
            )

        elif ext in [".mp4", ".mov", ".m4v", ".avi", ".mkv"]:
            media = InputMediaVideo(
                media=file_obj,
                caption=caption if idx == 0 else None,
                parse_mode="Markdown"
            )

        else:
            media = InputMediaDocument(
                media=file_obj,
                caption=caption if idx == 0 else None,
                parse_mode="Markdown"
            )

        media_group.append(media)

    for tg_id in tg_ids:

        if media_group:
            try:
                await bot.send_media_group(chat_id=tg_id, media=media_group)
            except Exception as e:
                print(f"Skipping invalid user {tg_id}: {e}")
                continue
        else:
            try:
                await bot.send_message(
                    chat_id=tg_id,
                    text=caption,
                    parse_mode="Markdown"
                )
            except Exception as e:
                print(f"Skipping invalid user {tg_id}: {e}")
                continue
