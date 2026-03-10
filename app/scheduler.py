from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import datetime
import pytz

# ⏰ Часовий пояс — Київ
kyiv_tz = pytz.timezone("Europe/Kyiv")

# 🔔 Повідомлення
messages = [
    "🕯 9:00 – загальнонаціональна хвилина мовчання. Присвятіть цю хвилину тим, хто віддав життя за Україну!",
]

# 🔄 Ротація за днем
def get_rotating_message():
    today = datetime.datetime.now(kyiv_tz).date()
    index = (today - datetime.date(2025, 1, 1)).days % len(messages)
    return messages[index]

# ⛓️ API для виклику з main
def get_random_message():
    return get_rotating_message()

# ✉️ Відправлення повідомлення
async def send_messages(bot, chat_id):
    now_utc = datetime.datetime.utcnow().strftime('%H:%M:%S')
    now_kyiv = datetime.datetime.now(kyiv_tz).strftime('%H:%M:%S')
    text = get_rotating_message()
    try:
        print(f"[UTC {now_utc} | Kyiv {now_kyiv}] ⏳ Надсилаємо повідомлення в чат {chat_id}")
        await bot.send_message(chat_id=chat_id, text=text)
        print(f"[Kyiv {now_kyiv}] ✅ Повідомлення успішно надіслано")
    except Exception as e:
        print(f"[Kyiv {now_kyiv}] ❌ ПОМИЛКА при надсиланні: {e}")

# ⏱️ Планувальник
async def setup_scheduler(bot, chat_id):
    scheduler = AsyncIOScheduler(timezone=kyiv_tz)

    # 🕘 Щодня з понеділка по п’ятницю о 08:55
    scheduler.add_job(
        send_messages,
        trigger=CronTrigger(day_of_week='mon-fri', hour=8, minute=55, timezone=kyiv_tz),
        args=[bot, chat_id]
    )

    scheduler.start()
