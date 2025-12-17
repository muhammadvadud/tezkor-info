import os
import sys
import asyncio
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

try:
    import django

    django.setup()
    logging.info("✅ Django muvaffaqiyatli ishga tushdi")
except Exception as e:
    logging.error(f"❌ Django setup xatosi: {e}")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from bot.handlers.send_otp import start_welcome_flow

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL")

if not BOT_TOKEN:
    logger.error("❌ BOT_TOKEN topilmadi!")
    sys.exit(1)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def on_startup():
    """Bot ishga tushganda"""
    try:
        from django.db import connections
        for conn in connections.all():
            conn.close()
        logger.info("✅ Database connectionlar tozalandi")

        me = await bot.get_me()
        logger.info(f"✅ Bot ishga tushdi: @{me.username}")
    except Exception as e:
        logger.error(f"❌ Startup xatosi: {e}")


async def on_shutdown():
    """Bot to'xtaganda"""
    try:
        from django.db import connections
        for conn in connections.all():
            conn.close()
        logger.info("✅ Database connectionlar yopildi")
    except Exception as e:
        logger.error(f"❌ Shutdown xatosi: {e}")


@dp.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    try:
        args = message.text.split(maxsplit=1)
        payload = args[1] if len(args) > 1 else None

        if payload and payload.startswith("register_"):
            await start_welcome_flow(message, state, payload)
            return
        if not WEB_APP_URL:
            await message.answer("Kechirasiz, vaqtinchalik xizmat mavjud emas.")
            return

        web_app_info = WebAppInfo(url=WEB_APP_URL)
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text="🚀 Platformaga kirish",
                    web_app=web_app_info
                )]
            ]
        )

        welcome_text = """🎯 Hurmatli tadbirkor, biznes egalari va investorlar!

Sizlar uchun O'zbekiston va xalqaro Biznes jamoasini birlashtiradigan innovatsion platforma taqdim etilmoqda — INFO TARGET GLOBALNET PORTAL 🚀

📊 Platformaning vazifasi: butun jaxon bo'ylab kompaniyalar rahbarlari bilan bevosita bog'lash.

✨ Platformaning Afzalliklari:
✔️ Aniq maqsadli auditoriya
✔️ Bevosita aloqa
✔️ Xalqaro kompaniyalar bazasi
✔️ Har xil formatlar
✔️ Express yetkazish
✔️ Shaffof analitika
"""

        await message.answer(welcome_text, reply_markup=keyboard)

    except Exception as e:

        logger.error(f"❌ Start handler xatosi: {e}", exc_info=True)
        await message.answer(f"❌ Xatolik yuz berdi.{e}")


async def main():
    """Asosiy funksiya"""
    logger.info("🚀 Bot ishga tushmoqda...")
    logger.info(f"🔑 Token: {BOT_TOKEN[:10]}...")

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    try:
        logger.info("📡 Polling boshlanmoqda...")
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=True
        )
    except KeyboardInterrupt:
        logger.info("⚠️ Bot Ctrl+C orqali to'xtatildi")
    except Exception as e:
        logger.error(f"❌ Polling xatosi: {e}", exc_info=True)
    finally:
        # Cleanup
        logger.info("🛑 Bot to'xtatilmoqda...")
        await on_shutdown()
        await bot.session.close()
        logger.info("✅ Bot to'xtatildi")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Dastur to'xtatildi")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)
