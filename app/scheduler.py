from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import random

messages = [
    "🕯 Ранок. Ця хвилина — про них.\nПро тих, завдяки кому ми живі.\n9:00 — хвилина мовчання.",
    "🕯 Нагадування\nО 9:00 — загальнонаціональна хвилина мовчання.\nВшануймо тих, хто віддав життя за Україну.",
    "🕯 Шановні колеги,\n\nНагадуємо, що сьогодні о 9:00 🕛 ми вшановуємо пам’ять загиблих хвилиною мовчання.\n\n🙏 Просимо зупинити робочі процеси та долучитися до цього символічного жесту поваги до тих, хто віддав своє життя за 🇺🇦 Україну.\n\n💙💛 Дякуємо за розуміння.",
    "🕯 9:00 — хвилина мовчання. Зупинімося. Згадаємо. Вшануймо.",
    "🙏 Згадуємо тих, хто віддав життя за нас. О 9:00 — хвилина мовчання. Не забудь зупинитися.",
    "🕯 Ціна нашої свободи — життя Героїв. 9:00 — вшануємо мовчанням.",
    "🕯 Нагадування: 9:00 — загальнонаціональна хвилина мовчання. Згадаємо наших захисників.",
    "🙏 Просимо о 9:00 зробити паузу в роботі — для вшанування пам’яті Героїв України.",
    "🕛 9:00 — хвилина мовчання. Віддаймо шану тим, хто поклав життя за Україну. 💙💛"
]

async def send_messages(bot, chat_id):
    msg = random.choice(messages)
    await bot.send_message(chat_id=chat_id, text=msg)

async def setup_scheduler(bot, chat_id):
    scheduler = AsyncIOScheduler(timezone="Europe/Kyiv")
    trigger = CronTrigger(day_of_week="mon-fri", hour=8, minute=55)
    scheduler.add_job(send_messages, trigger, args=[bot, chat_id])
    scheduler.start()
