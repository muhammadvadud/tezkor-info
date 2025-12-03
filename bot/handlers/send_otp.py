from aiogram import types, Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from bot.state_utils.register_state import RegisterState
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

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

    try:
        from core.services.send_otp_bot import get_or_return_sms_code

        logger.info(f"🔍 SMS kod tekshirilmoqda: {phone_number}")

        from channels.db import database_sync_to_async

        check = await database_sync_to_async(get_or_return_sms_code)(phone_number)

        logger.info(f"✅ Natija: {check} (type: {type(check)})")

        remove_kb = ReplyKeyboardRemove()

        if check and check is not False:
            text = f"SMS kod:||`{check}`||"

            await message.answer(text=text,
                                 parse_mode="MarkdownV2",
                                 )
            await state.clear()

        else:
            await message.answer(
                "❌ Uzr, sizga hech qanday kod yuborilmagan!",
                reply_markup=remove_kb
            )
            await state.clear()

    except ImportError as e:
        logger.error(f"❌ Import xatosi: {e}")
        await message.answer(f"⚠️ Xatolik: Funksiya topilmadi\n{e}")

    except Exception as e:
        logger.error(f"❌ Xatolik yuz berdi: {e}", exc_info=True)
        await message.answer(
            f"⚠️ Xatolik yuz berdi:\n{str(e)}",
            reply_markup=ReplyKeyboardRemove()
        )
