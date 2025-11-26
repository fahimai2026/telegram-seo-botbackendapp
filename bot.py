import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Update
from fastapi import APIRouter, Request
import logging

# Load Telegram Token from environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("TELEGRAM_WEBHOOK_URL")

# Initialize Bot and Dispatcher
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Bot Command Handlers ---

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    """
    Handler for the /start command.
    Sends a welcome message to the user.
    """
    try:
        await message.reply(
            "👋 হ্যালো! আমি আপনার SEO বট।\n\n"
            "আমি আপনাকে YouTube ভিডিওর জন্য SEO অপ্টিমাইজড টাইটেল এবং ডেসক্রিপশন জেনারেট করতে সাহায্য করতে পারি।\n"
            "শুরু করতে আপনার ভিডিওর টাইটেল বা টপিক লিখুন।"
        )
        logger.info(f"Sent welcome message to user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error sending welcome message: {e}")

@dp.message()
async def echo_handler(message: types.Message):
    """
    Echo handler for testing.
    Replies with the same message content.
    (You can replace this with your SEO logic later)
    """
    try:
        await message.answer(f"আপনি বলেছেন: {message.text}")
    except Exception as e:
        logger.error(f"Error in echo handler: {e}")


# --- FastAPI Router for Webhook ---

telegram_webhook_router = APIRouter()

@telegram_webhook_router.post("/")  # This path matches /webhook/telegram in main.py
async def telegram_webhook_handler(request: Request):
    """
    Endpoint to receive updates from Telegram Webhook.
    """
    try:
        # Get the update from the request body
        update_data = await request.json()
        
        # Validate update data
        if not update_data:
             logger.warning("Received empty update data")
             return {"status": "ignored"}

        # Create Update object
        update = Update(**update_data)
        
        # Feed the update to the dispatcher
        await dp.feed_update(bot, update)
        
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error processing update: {e}")
        return {"status": "error", "message": str(e)}

# Function to set webhook on startup (optional, but good for auto-setup)
async def set_webhook():
    if not WEBHOOK_URL:
        logger.warning("WEBHOOK_URL is not set. Skipping webhook setup.")
        return
        
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        logger.info(f"Setting webhook to: {WEBHOOK_URL}")
        await bot.set_webhook(WEBHOOK_URL)
    else:
        logger.info("Webhook is already set correctly.")