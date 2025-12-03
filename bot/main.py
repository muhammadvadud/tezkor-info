import os
import sys
import asyncio
import logging
from signal import signal, SIGINT, SIGTERM

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

try:
    import django

    django.setup()
except Exception as e:
    print(f"❌ Django setup xatosi: {e}")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.fsm.context import FSMContext

from bot.handlers.send_otp import start_welcome_flow
from bot.handlers.send_otp import router as send_otp_router

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL")

if not BOT_TOKEN:
    logger.error("❌ BOT_TOKEN topilmadi!")
    sys.exit(1)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart(deep_link=True))
async def handle_deep_link(message: types.Message, command: CommandObject, state: FSMContext):
    raw_payload = command.args
    if raw_payload == "register":
        await start_welcome_flow(message, state)
    else:
        await start_handler(message)


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    if not WEB_APP_URL:
        logger.warning("⚠️ WEB_APP_URL o'rnatilmagan")
        await message.answer("Kechirasiz, vaqtinchalik xizmat mavjud emas.")
        return

    web_app_info = WebAppInfo(url=WEB_APP_URL)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Platformaga kirish", web_app=web_app_info)],
        ]
    )

    await message.answer(
        """Hurmatli tadbirkor, biznes egalari va investorlar!

Sizlar uchun O'zbekiston va xalqaro Biznes jamoasini birlashtiradigan innovatsion platforma taqdim etilmoqda — INFO TARGET GLOBALNET PORTAL

🚀 INFO TARGET GLOBALNET PORTAL 

Platformaning vazifasi: butun jaxon bo'ylab kompaniyalar rahbarlari bilan bevosita bog'lash.

Biznesingiz haqida maqsadli auditoriyaga Telegram orqali to'g'ridan-to'g'ri xabar yuborish imkoniyati yaratiladi.

🎯 Platformaning Afzalliklari

✔️ Aniq maqsadli auditoriya — rahbarlar, direktorlar, tadbirkorlar va top-menejerlar
✔️ Bevosita aloqa — reklama xabarlari Telegramdagi shaxsiy akkauntlarga yetkaziladi
✔️ Xalqaro kompaniyalar bazasi O'zbekiston va chet davlatlari
✔️ Har xil formatlar — poster, video, prezentatsiya, hujjat
✔️ Express yetkazish — vaqt va pulni tejash
✔️ Shaffof analitika va real natijalar""",
        reply_markup=keyboard
    )


async def shutdown():
    logger.info("🛑 Bot to'xtatilmoqda...")
    await bot.session.close()
    logger.info("✅ Bot to'xtatildi")


async def main():
    logger.info("🚀 Bot ishga tushmoqda...")
    logger.info(f"🔑 Token: {BOT_TOKEN[:10]}...")

    dp.include_router(send_otp_router)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except (KeyboardInterrupt, SystemExit):
        logger.info("⚠️ Bot to'xtatildi")
    except Exception as e:
        logger.error(f"❌ Xatolik: {e}", exc_info=True)
    finally:
        await shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Ctrl+C orqali to'xtatildi")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)
