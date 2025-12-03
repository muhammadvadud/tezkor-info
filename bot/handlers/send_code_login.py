from aiogram import Bot


async def send_otp_to_users(bot: Bot, chat_ids: list[int], code: str):
    """
    Aiogram orqali bir nechta userlarga OTP yuborish funksiyasi.

    bot: main.py dagi Bot obyekt
    chat_ids: [12345, 67890, ...]
    code: yuboriladigan matn (OTP)
    """
    text = f"🔐 Sizning tasdiqlash kodingiz: `{code}`"

    for user_id in chat_ids:
        try:
            await bot.send_message(chat_id=user_id, text=text, parse_mode="Markdown")
        except Exception as e:
            print(f"Xatolik: {user_id} ga yuborilmadi. Sabab: {e}")
