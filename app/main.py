import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums.parse_mode import ParseMode

from app.scheduler import setup_scheduler, get_random_message

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID_RAW = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID_RAW:
    raise RuntimeError("❌ BOT_TOKEN або CHAT_ID не встановлено у секретах Fly.io!")

try:
    CHAT_ID = int(CHAT_ID_RAW)
except ValueError:
    raise RuntimeError(f"❌ CHAT_ID має бути цілим числом, зараз: {CHAT_ID_RAW}")

print(f"✅ BOT запущено з CHAT_ID: {CHAT_ID}")

# Без кастомної сесії — щоб не падало на несумісній версії aiogram
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("ping"))
async def ping_command(message: types.Message):
    test_message = get_random_message()
    await message.answer(f"✅ Бот працює!\n\n{test_message}", parse_mode=ParseMode.HTML)


@dp.message(Command("testsend"))
async def testsend_command(message: types.Message):
    try:
        text = f"🧪 Тестове повідомлення\n\n{get_random_message()}"
        await bot.send_message(chat_id=CHAT_ID, text=text, parse_mode=ParseMode.HTML)
        await message.answer("✅ Тестове повідомлення відправлено в цільовий чат")
    except Exception as e:
        await message.answer(f"❌ Не вдалося надіслати в цільовий чат:\n{type(e).__name__}: {e}")


async def main():
    await setup_scheduler(bot, CHAT_ID)
    print("⏳ Очікуємо запланованих подій...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
