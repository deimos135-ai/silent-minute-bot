from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import random
import datetime
import pytz

# ⏰ Timezone Kyiv (через pytz)
kyiv_tz = pytz.timezone("Europe/Kyiv")

# 🔔 Повідомлення
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

    # 🧪 ТЕСТОВЕ — кожну хвилину (видали перед продом)
   # scheduler.add_job(
      #  send_messages,
     #   trigger=CronTrigger(minute="*", timezone=kyiv_tz),
      #  args=[bot, chat_id]
    #)

    # 🕘 БОЙОВЕ — 8:55 Пн-Пт (закоментовано на час тесту)
     scheduler.add_job(
         send_messages,
         trigger=CronTrigger(day_of_week='mon-fri', hour=10, minute=58, timezone=kyiv_tz),
         args=[bot, chat_id]
     )

    scheduler.start()
