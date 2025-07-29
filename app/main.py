import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from .scheduler import setup_scheduler, get_random_message

BOT_TOKEN = os.getenv("BOT_TOKEN_NEW")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message(Command("ping"))
async def ping_command(message: types.Message):
    test_message = get_random_message()
    response = "✅ Бот працює! Ось приклад повідомлення:\n\n" + test_message
    await message.answer(response)

async def main():
    await setup_scheduler(bot, CHAT_ID)
    print("✅ Silent Minute Bot запущено. Очікуємо запланованих подій та команд...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
