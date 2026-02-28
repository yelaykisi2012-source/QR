import asyncio
import logging
import urllib.parse
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

# TOKENNI SHU YERGA YOZING
BOT_TOKEN = "8671059780:AAFP61Cb8fMZ24CvdgbbqZO4rKemHb48EG0"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    # Foydalanuvchining to'liq ismini olish
    user_full_name = message.from_user.full_name

    await message.answer(f"Salom, {user_full_name}! 👋\n️\n\n Menga matn yoki raqam yuboring, darhol QR chiqarib beraman!")


@dp.message()
async def handle_message(message: types.Message):
    if not message.text:
        return

    text = message.text.strip()

    # Telefon raqam tahlili
    if text.startswith('+') or (text.isdigit() and len(text) > 5):
        qr_data = f"tel:{text}" if text.startswith('+') else f"tel:+{text}"
    else:
        qr_data = text

    # Eng ishonchli yangi API manzili
    encoded_text = urllib.parse.quote(qr_data)
    # Bu API hozir aniq ishlayapti:
    qr_link = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={encoded_text}"

    try:
        # Telegramga rasm sifatida yuborish
        await message.reply_photo(
            photo=qr_link,
            caption=f"✅ QR Kod tayyor!\nMa'lumot: `{text}`",
            parse_mode="Markdown"
        )
    except Exception as e:
        logging.error(f"Xatolik: {e}")
        # Agar rasm yuklanmasa, linkni yuboramiz
        await message.reply(f"Rasm yuklashda muammo bo'ldi, lekin mana havola: {qr_link}")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print("✅ Bot yangi API bilan ishga tushdi!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
