import os
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode

# bot.py থেকে router ইমপোর্ট করুন
from bot import router as bot_router 

load_dotenv()

# লগিং চালু করুন (এরর দেখার জন্য খুব জরুরি)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# বট এবং ডিসপ্যাচার তৈরি
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# --- গুরত্বপূর্ণ: রাউটারটি ডিসপ্যাচারে যুক্ত করা ---
dp.include_router(bot_router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # অ্যাপ চালু হলে ওয়েবহুক সেট হবে
    await bot.set_webhook(WEBHOOK_URL)
    logger.info(f"Webhook set to: {WEBHOOK_URL}")
    yield
    # অ্যাপ বন্ধ হলে ওয়েবহুক ডিলিট হবে
    await bot.delete_webhook()
    logger.info("Webhook removed")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Bot is running properly!"}

@app.post("/webhook")
async def bot_webhook(request: Request):
    try:
        update_data = await request.json()
        telegram_update = types.Update(**update_data)
        
        # ডিসপ্যাচারে আপডেট পাঠানো
        await dp.feed_update(bot, telegram_update)
        
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error handling update: {e}")
        return {"status": "error", "message": str(e)}