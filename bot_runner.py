# bot_runner.py

import os
import asyncio
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler

from main import run_parallel_scraping  # импорт функции из main.py

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))
SCRAPE_INTERVAL_SECONDS = int(os.getenv("SCRAPE_INTERVAL_SECONDS", "300"))


async def start(update, context):
    await update.message.reply_text("Бот запущен, мониторю OLX.")


async def check(update, context):
    await update.message.reply_text("Запускаю внеплановый проход по категориям...")
    stats = run_parallel_scraping()
    await update.message.reply_text(
        f"Готово: {stats['total_ads']} объявлений, "
        f"{stats['total_new']} новых, "
        f"{stats['total_deals']} выгодных."
    )


async def scheduled_scrape(context):
    stats = run_parallel_scraping()
    # если есть выгодные — шлёшь в чат
    if stats["total_deals"] > 0:
        await context.bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=(
                f"Найдены новые выгодные объявления: "
                f"{stats['total_deals']} шт."
            ),
        )


async def main():
    app = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))

    # бесконечный цикл через job_queue
    app.job_queue.run_repeating(
        scheduled_scrape,
        interval=SCRAPE_INTERVAL_SECONDS,
        first=0,
    )

    print("Bot is starting, polling Telegram...")
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
