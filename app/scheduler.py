from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import random
import datetime

# 🔔 Варіанти повідомлень
messages = [
    "🕯 Ранок. Хвилина мовчання — на честь Героїв. 🇺🇦 9:00",
    "🕯 Нагадування: о 9:00 — хвилина мовчання за полеглими.",
    "🕛 Зупинімося на хвилину. Вшануймо пам’ять Героїв України.",
    "🕯 9:00 — загальнонаціональна хвилина мовчання. Не забудь."
]

def get_random_message():
    return random.choice(messages)

# ✉️ Відправка повідомлення
async def send_messages(bot, chat_id):
    now = datetime.datetime.now().strftime('%H:%M:%S')
    text = get_random_message()
    try:
        print(f"[{now}] ⏳ Надсилаємо повідомлення в чат {chat_id}")
        await bot.send_message(chat_id=chat_id, text=text)
        print(f"[{now}] ✅ Повідомлення успішно надіслано")
    except Exception as e:
        print(f"[{now}] ❌ ПОМИЛКА при надсиланні: {e}")

# ⏱️ Налаштування планувальника
async def setup_scheduler(bot, chat_id):
    scheduler = AsyncIOScheduler(timezone="Europe/Kyiv")

    # Основне повідомлення (о 8:55 щодня, пн-пт)
    scheduler.add_job(
        send_messages,
        trigger=CronTrigger(day_of_week='mon-fri', hour=10, minute=33),
        args=[bot, chat_id]
    )

    # 🧪 Тестове кожні 2 хвилини (видали в проді)
    # scheduler.add_job(send_messages, CronTrigger(minute="*/2"), args=[bot, chat_id])

    scheduler.start()
