from aiogram import types, Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from bot.state_utils.register_state import RegisterState
from asgiref.sync import sync_to_async
from django.db import close_old_connections

import logging

logger = logging.getLogger(__name__)

router = Router()


async def start_welcome_flow(message: types.Message, state: FSMContext):
    WELCOME_TEXT = (
        "Assalomu alaykum! 👋\n"
        "Botimizga xush kelibsiz! 😊\n\n"
        "Sizni nomeringizni tasdiqlash uchun iltimos pastdagi '📲 Raqamni yuborish' tugmasini bosing."
    )
    contact_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📲 Raqamni yuborish", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await state.set_state(RegisterState.wait_phone)
    await message.answer(WELCOME_TEXT, reply_markup=contact_keyboard)


from django.db import transaction


async def safe_db_call(func, *args, **kwargs):
    """
    Atomik tranzaksiya bilan database operatsiyalari
    """
    connection = None
    try:
        # Eski connectionlarni yopish
        await sync_to_async(close_old_connections)()

        @sync_to_async
        def execute_in_transaction():
            from django.db import connection as db_conn
            nonlocal connection
            connection = db_conn

            with transaction.atomic():
                return func(*args, **kwargs)

        result = await execute_in_transaction()
        return result

    except Exception as e:
        logger.error(f"Database xatolik: {e}", exc_info=True)
        raise
    finally:
        # Connection'ni majburiy yopish
        if connection and not connection.closed:
            await sync_to_async(connection.close)()
        await sync_to_async(close_old_connections)()


@router.message(RegisterState.wait_phone)
async def check_phone_number(message: types.Message, state: FSMContext):
    if not message.contact:
        contact_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📲 Raqamni yuborish", request_contact=True)]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await message.answer("Iltimos pastdagi tugmani bosing 👇", reply_markup=contact_keyboard)
        return

    phone_number = message.contact.phone_number.lstrip('+')
    logger.info(f"📞 Telefon raqam qabul qilindi: {phone_number}")

    remove_kb = ReplyKeyboardRemove()

    try:
        from core.services.send_otp_bot import get_or_return_sms_code
        from django.db import connection

        logger.info(f"🔍 SMS kod tekshirilmoqda: {phone_number}")

        # Connection'larni tozalash
        await sync_to_async(close_old_connections)()

        # SMS kodni olish
        @sync_to_async
        def get_code():
            try:
                with transaction.atomic():
                    return get_or_return_sms_code(phone_number)
            finally:
                # Connection'ni yopish
                if not connection.closed:
                    connection.close()

        check = await get_code()

        logger.info(f"✅ Natija: {check} (type: {type(check)})")

        if check and check is not False:
            text = f"SMS kod:||`{check}`||"
            await message.answer(
                text=text,
                parse_mode="MarkdownV2",
                reply_markup=remove_kb
            )
        else:
            await message.answer(
                "❌ Uzr, sizga hech qanday kod yuborilmagan!",
                reply_markup=remove_kb
            )

    except ImportError as e:
        logger.error(f"❌ Import xatosi: {e}")
        await message.answer(f"⚠️ Xatolik: Funksiya topilmadi\n{e}", reply_markup=remove_kb)

    except Exception as e:
        logger.error(f"❌ Xatolik yuz berdi: {e}", exc_info=True)
        await message.answer(
            f"⚠️ Xatolik yuz berdi:\n{str(e)}",
            reply_markup=remove_kb
        )

    finally:
        # Har holda state'ni tozalash va connectionlarni yopish
        await state.clear()
        await sync_to_async(close_old_connections)()
