from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import random
import datetime
import pytz

# ⏰ Часовий пояс — Київ
kyiv_tz = pytz.timezone("Europe/Kyiv")

# 🔔 Повідомлення на вибір
messages = [
    "🕯 Щодня о 9:00 — хвилина мовчання. Згадаємо Героїв, що віддали життя за 🇺🇦",
    "🕛 9:00 — час зупинитися і вшанувати полеглих. Пам’ятаємо. 💙💛",
    "🕯 Момент тиші. 9:00 — хвилина мовчання за тими, хто не повернувся з бою.",
    "🙏 О 9:00 — приєднайся до хвилини мовчання. Віддай шану нашим Захисникам.",
    "🕛 9:00 — схилімо голови в пам'ять про тих, хто захищав нашу свободу.",
    "🕯 Ціна миру — життя Героїв. 9:00 — зупинимось і вшануємо.",
    "🕯 Вшануймо тишею тих, хто виборов нам ранок. 9:00 — хвилина мовчання.",
    "🙏 Зупинись на мить о 9:00. Герої не вмирають.",
    "🕛 9:00 — символічна тиша. Пам’ятаємо кожного, хто боровся за 🇺🇦",
    "🕯 Кожного дня о 9:00 — пам’ятаємо тих, хто дав нам новий день."
]

def get_random_message():
    return random.choice(messages)

# ✉️ Відправлення повідомлення
async def send_messages(bot, chat_id):
    now_utc = datetime.datetime.utcnow().strftime('%H:%M:%S')
    now_kyiv = datetime.datetime.now(kyiv_tz).strftime('%H:%M:%S')
    text = get_random_message()
    try:
        print(f"[UTC {now_utc} | Kyiv {now_kyiv}] ⏳ Надсилаємо повідомлення в чат {chat_id}")
        await bot.send_message(chat_id=chat_id, text=text)
        print(f"[Kyiv {now_kyiv}] ✅ Повідомлення успішно надіслано")
    except Exception as e:
        print(f"[Kyiv {now_kyiv}] ❌ ПОМИЛКА при надсиланні: {e}")

# ⏱️ Планувальник
async def setup_scheduler(bot, chat_id):
    scheduler = AsyncIOScheduler(timezone=kyiv_tz)

    # 🕘 Бойове повідомлення — щодня з понеділка по п’ятницю о 08:55
    scheduler.add_job(
        send_messages,
        trigger=CronTrigger(day_of_week='mon-fri', hour=11, minute=15, timezone=kyiv_tz),
        args=[bot, chat_id]
    )

    scheduler.start()
