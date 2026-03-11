import asyncio
import datetime
import pytz

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

# Часовий пояс — Київ
kyiv_tz = pytz.timezone("Europe/Kyiv")

# Повідомлення
messages = [
    "🕯 9:00 – загальнонаціональна хвилина мовчання. Присвятіть цю хвилину тим, хто віддав життя за Україну!",
]

# Ротація повідомлень по дню
def get_rotating_message():
    today = datetime.datetime.now(kyiv_tz).date()
    index = (today - datetime.date(2025, 1, 1)).days % len(messages)
    return messages[index]

# Використовується в main.py для /ping
def get_random_message():
    return get_rotating_message()

# Надсилання повідомлення з повторними спробами
async def send_messages(bot, chat_id):
    now_utc = datetime.datetime.utcnow().strftime("%H:%M:%S")
    now_kyiv = datetime.datetime.now(kyiv_tz).strftime("%H:%M:%S")
    text = get_rotating_message()

    print(f"[UTC {now_utc} | Kyiv {now_kyiv}] ⏳ Надсилаємо повідомлення в чат {chat_id}")

    max_attempts = 5
    delay_seconds = 10

    for attempt in range(1, max_attempts + 1):
        try:
            await bot.send_message(chat_id=chat_id, text=text)
            print(f"[Kyiv {now_kyiv}] ✅ Повідомлення успішно надіслано з {attempt}-ї спроби")
            return
        except Exception as e:
            print(f"[Kyiv {now_kyiv}] ⚠️ Спроба {attempt}/{max_attempts} не вдалася: {type(e).__name__}: {e}")

            if attempt < max_attempts:
                await asyncio.sleep(delay_seconds)
            else:
                print(f"[Kyiv {now_kyiv}] ❌ Не вдалося надіслати повідомлення після {max_attempts} спроб")

# Планувальник
async def setup_scheduler(bot, chat_id):
    scheduler = AsyncIOScheduler(timezone=kyiv_tz)

    scheduler.add_job(
        send_messages,
        trigger=CronTrigger(
            day_of_week="mon-fri",
            hour=9,
            minute=0,
            timezone=kyiv_tz
        ),
        args=[bot, chat_id],
        misfire_grace_time=300,
        coalesce=True,
        max_instances=1,
    )

    scheduler.start()
    print("✅ Scheduler запущено: повідомлення будуть надсилатися у будні о 09:00 за Києвом")
