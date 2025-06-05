import asyncio
import logging
from bot.handlers import setup_handlers
from telegram.ext import Application
from config.settings import TELEGRAM_TOKEN
from bot.queue_manager import download_worker
from utils.logger_config import setup_logging
from telegram.request import HTTPXRequest
import nest_asyncio

setup_logging()

logger = logging.getLogger(__name__)

nest_asyncio.apply()

async def run_bot():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    setup_handlers(application)
    asyncio.create_task(download_worker())
    print("Bot is running...")
    await application.run_polling()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_bot())
