import asyncio
import logging
import os
from aiogram.types import FSInputFile, InputMediaPhoto, InputMediaVideo

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.filters import Command

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    web_app_info = WebAppInfo(url=os.getenv("WEB_APP_URL"))
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Platformaga kirish", web_app=web_app_info)],
        ]
    )

    await message.answer(
        """Hurmatli tadbirkor, biznes egalari va investorlar!



Sizlar uchun O‘zbekiston va xalqaro Biznes jamoasini birlashtiradigan innovatsion platforma taqdim etilmoqda — INFO TARGET GLOBALNET PORTAL



🚀 INFO TARGET GLOBALNET PORTAL 

Platformaning vazifasi: butun jaxon bo‘ylab kompaniyalar rahbarlari bilan bevosita bog‘lash.

Biznesingiz haqida maqsadli auditoriyaga Telegram orqali to‘g‘ridan-to‘g‘ri xabar yuborish imkoniyati yaratiladi.



🎯 Platformaning Afzalliklari

✔️ Aniq maqsadli auditoriya — rahbarlar, direktorlar, tadbirkorlar va top-menejerlar

✔️ Bevosita aloqa — reklama xabarlari Telegramdagi shaxsiy akkauntlarga yetkaziladi

✔️ Xalqaro kompaniyalar bazasi O‘zbekiston va chet davlatlari

✔️ Har xil formatlar — poster, video, prezentatsiya, hujjat

✔️ Express yetkazish — vaqt va pulnu tejash

✔️ Shaffof analitika va real natijalar
        """, reply_markup=keyboard
    )


async def send_ad_bot(ad_data, files, tg_ids, bot: Bot):
    caption = f"""
🆕 Yangi reklama!

📌 <b>{ad_data['title']}</b>

{ad_data['description']}
{ad_data['username']}
{ad_data['phone']}
"""

    # Agar fayllar bo‘lmasa → text yuboriladi
    if not files:
        for tg_id in tg_ids:
            try:
                await bot.send_message(tg_id, caption, parse_mode="HTML")
            except Exception as e:
                print(f"[ERROR] Matn yuborilmadi ({tg_id}): {e}")
        return

    # Bitta media-group yasaymiz
    media_group = []

    for index, file_path in enumerate(files):
        ext = os.path.splitext(file_path)[1].lower()
        input_file = FSInputFile(file_path)

        # Birinchi media → caption bo‘ladi
        if ext in [".jpg", ".jpeg", ".png", ".webp"]:
            media = InputMediaPhoto(media=input_file)
        elif ext in [".mp4", ".mov", ".avi"]:
            media = InputMediaVideo(media=input_file)
        else:
            # Noma'lum format → document bo‘lib ketadi
            media = InputMediaPhoto(media=input_file)

        if index == 0:  # faqat birinchi rasm/video caption oladi
            media.caption = caption
            media.parse_mode = "HTML"

        media_group.append(media)

    # Har bir userga media-group yuboramiz
    for tg_id in tg_ids:
        try:
            await bot.send_media_group(chat_id=tg_id, media=media_group)
        except Exception as e:
            print(f"[ERROR] Media-group yuborilmadi ({tg_id}): {e}")


async def main():
    logger.info("Bot ishga tushmoqda...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
