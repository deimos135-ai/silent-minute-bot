from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import pytz
import random
import logging

from app.bot import send_message
from app.constants import MESSAGES, CHAT_ID

kyiv_tz = pytz.timezone("Europe/Kyiv")
scheduler = BackgroundScheduler(timezone=kyiv_tz)

def get_random_message():
    return random.choice(MESSAGES)

def job_send_random_message():
    now = datetime.now(kyiv_tz)
    logging.info(f"[Kyiv {now.strftime('%H:%M:%S')}] ⏳ Надсилаємо повідомлення в чат {CHAT_ID}")
    message = get_random_message()
    send_message(CHAT_ID, message)
    logging.info(f"[Kyiv {now.strftime('%H:%M:%S')}] ✅ Повідомлення успішно надіслано")

def setup_scheduler():
    scheduler.add_job(
        job_send_random_message,
        trigger=CronTrigger(day_of_week='mon-fri', hour=11, minute=6, timezone=kyiv_tz),
        id="daily_silent_minute"
    )

    # scheduler.add_job(  # Розкоментуй якщо хочеш щохвилини для тесту
    #     job_send_random_message,
    #     trigger=CronTrigger(minute="*", timezone=kyiv_tz),
    #     id="test_every_minute"
    # )

    scheduler.start()
