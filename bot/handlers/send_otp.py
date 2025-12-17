from aiogram import types
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from django.db import transaction, close_old_connections
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
import logging
import os

WEB_APP_URL = os.getenv("WEB_APP_URL")
logger = logging.getLogger(__name__)


async def db_call(func, *args, **kwargs):
    """Universal database wrapper"""
    try:
        @sync_to_async
        def execute():
            with transaction.atomic():
                return func(*args, **kwargs)

        return await execute()
    finally:
        await sync_to_async(close_old_connections)()


async def start_welcome_flow(message: types.Message, state: FSMContext, payload, payload_type):
    WELCOME_TEXT = (
        "Assalomu alaykum! 👋\n"
        "Botimizga xush kelibsiz! 😊\n"
    )

    phone = None
    try:
        if payload and payload.startswith(f"{payload_type}_"):
            phone = payload.split("_", 1)[1]
        else:
            await message.answer(
                WELCOME_TEXT +
                "❌ Telefon raqam topilmadi."
            )
            return

        from core.services.send_otp_bot import get_or_return_sms_code

        async def get_code():
            return await db_call(get_or_return_sms_code, phone)

        code = await get_code()

        if code:
            URL = f"{WEB_APP_URL}/{payload_type}?code={code}&phone={phone}"
            web_app_info = WebAppInfo(url=URL)

            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Parol Tasdiqlash", web_app=web_app_info)],
                ]
            )
            await message.answer(
                WELCOME_TEXT +
                f"Sizning kodingiz:\n\nTasdiqlash uchun kod: <code>{code}</code>\n\n{URL}",
                parse_mode="HTML",
                reply_markup=keyboard,
            )
        else:
            await message.answer(
                WELCOME_TEXT +
                "❌ Ushbu raqamga hech qanday kod yuborilmagan."
            )

    except Exception as e:
        logger.error(e, exc_info=True)
        await message.answer(
            WELCOME_TEXT +
            f"⚠️ Xatolik yuz berdi. Iltimos keyinroq urinib ko‘ring.{e}"
        )

    finally:
        await state.clear()
        await sync_to_async(close_old_connections)()
