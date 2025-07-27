import asyncio
import os
from aiogram import Bot, Dispatcher
from .scheduler import setup_scheduler

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def main():
    await setup_scheduler(bot, CHAT_ID)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
