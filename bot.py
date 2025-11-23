# backend/app/bot.py
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import settings
from db import get_or_create_user, check_subscription
from rate_limiter import allow_request, get_cached_result, cache_result
from ai_client import generate_seo

bot = Bot(token=settings.TELEGRAM_TOKEN, parse_mode="HTML")
dp = Dispatcher()

@dp.message(Command(commands=["start"]))
async def start(message: types.Message):
    await message.answer(
        "👋 Welcome! Send me your old YouTube title, "
        "and I'll return SEO optimized Title, Description & Hashtags."
    )

@dp.message()
async def handle_title(message: types.Message):
    telegram_id = str(message.from_user.id)
    username = message.from_user.username
    user_id = get_or_create_user(telegram_id, username)

    # Subscription check
    tier = check_subscription(user_id)
    if tier == "free" and not allow_request(telegram_id):
        await message.answer(
            "⚠️ You reached your free daily limit. Upgrade to Pro for unlimited generation."
        )
        return

    title = message.text.strip()
    await message.answer("⏳ Generating SEO optimized content...")

    # Check cache
    cached = get_cached_result(title)
    if cached:
        data = cached
    else:
        # Call AI
        try:
            outputs = await asyncio.to_thread(generate_seo, title, "bn", "energetic", 1)
            data = outputs[0]
            cache_result(title, data)
        except Exception as e:
            await message.answer(f"❌ Error generating: {e}")
            return

    seo_title = data.get("title", "")
    description = data.get("description", "")
    hashtags = " ".join(data.get("hashtags", []))

    response_text = f"✨ <b>SEO Title:</b>\n{seo_title}\n\n" \
                    f"📝 <b>Description:</b>\n{description}\n\n" \
                    f"🏷️ <b>Hashtags:</b>\n{hashtags}"
    await message.answer(response_text)

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
