import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from .scheduler import setup_scheduler

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Обробник команди /ping
@dp.message(Command("ping"))
async def ping_command(message: types.Message):
    await message.answer("✅ Бот працює! Готовий до розсилки.")

async def main():
    await setup_scheduler(bot, CHAT_ID)
    print("✅ Silent Minute Bot запущено. Очікуємо запланованих подій та команд...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
