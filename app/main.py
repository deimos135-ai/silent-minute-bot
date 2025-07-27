import asyncio
import os
from aiogram import Bot
from .scheduler import setup_scheduler

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

async def main():
    await setup_scheduler(bot, CHAT_ID)
    await asyncio.Event().wait()  # Бот працює вічно, нічого не слухає

if __name__ == "__main__":
    asyncio.run(main())
