import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from app.scheduler import setup_scheduler, get_random_message

# ⏬ Отримуємо змінні з Fly.io секретів
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID_RAW = os.getenv("CHAT_ID_NEW")

if not BOT_TOKEN or not CHAT_ID_RAW:
    raise RuntimeError("❌ BOT_TOKEN або CHAT_ID не встановлено у секретах Fly.io!")

try:
    CHAT_ID = int(CHAT_ID_RAW)
except ValueError:
    raise RuntimeError(f"❌ CHAT_ID має бути цілим числом, зараз: {CHAT_ID_RAW}")

print(f"✅ BOT запущено з CHAT_ID: {CHAT_ID}")

# 🔧 Ініціалізація бота
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# 🔁 Команда для перевірки бота
@dp.message(Command("ping"))
async def ping_command(message: types.Message):
    test_message = get_random_message()
    await message.answer(f"✅ Бот працює!\n\n{test_message}")

# 🧠 Основна логіка
async def main():
    await setup_scheduler(bot, CHAT_ID)
    print("⏳ Очікуємо запланованих подій...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
