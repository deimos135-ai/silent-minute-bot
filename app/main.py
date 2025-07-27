import asyncio
import os
from aiogram import Bot
from .scheduler import setup_scheduler

# Отримуємо токен і чат ID з середовища
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Ініціалізуємо бота
bot = Bot(token=BOT_TOKEN)

async def main():
    # Запускаємо планувальник
    await setup_scheduler(bot, CHAT_ID)

    # Лог у консоль (видно в логах Fly.io)
    print("✅ Silent Minute Bot запущено. Очікуємо запланованих подій...")

    # Нескінченний цикл, щоб контейнер не завершувався
    while True:
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
