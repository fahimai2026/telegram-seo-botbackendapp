import os
import aiohttp
import asyncio
from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart

router = Router()

# API Key পরিবেশ থেকে নেওয়া
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

# চেক করার জন্য মডেলের তালিকা
MODELS_TO_TRY = [
    "gemini-1.5-flash",  # লেটেস্ট এবং ফাস্ট
    "gemini-pro",        # সবচেয়ে স্টেবল (সবাই পায়)
    "gemini-1.5-pro"     # পাওয়ারফুল
]

# --- ডাইরেক্ট API কল ফাংশন (স্মার্ট সুইচিং) ---
async def call_gemini_api(prompt):
    if not GOOGLE_API_KEY:
        return "⚠️ API Key পাওয়া যায়নি! Render-এ চেক করুন।"

    async with aiohttp.ClientSession() as session:
        # সব মডেল দিয়ে একে একে চেষ্টা করবে
        for model in MODELS_TO_TRY:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GOOGLE_API_KEY}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
            
            try:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        # যদি কাজ হয়, রেজাল্ট রিটার্ন করবে
                        data = await response.json()
                        return data['candidates'][0]['content']['parts'][0]['text']
                    else:
                        # যদি এই মডেল কাজ না করে, পরের মডেলে যাবে
                        print(f"Failed with {model}, trying next...")
                        continue
            except Exception:
                continue

    return "⚠️ দুঃখিত, আপনার API Key দিয়ে কোনো মডেলই কাজ করছে না। দয়া করে নতুন Gmail দিয়ে নতুন Key খুলুন।"

# -------------------------------------------

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="সাহায্য চাই")]],
        resize_keyboard=True
    )
    welcome_msg = (
        f"👋 **স্বাগতম, {message.from_user.first_name}!**\n\n"
        "আমি Google Gemini (Auto) ⚡ দ্বারা চালিত আপনার SEO এক্সপার্ট।\n"
        "যেকোনো ভিডিওর **টাইটেল** পাঠান, আমি দিচ্ছি:\n"
        "✅ ৩টি অপ্টিমাইজড টাইটেল\n✅ এসইও ডেসক্রিপশন\n✅ ভাইরাল ট্যাগ"
    )
    await message.answer(welcome_msg, reply_markup=keyboard)

@router.message(F.text)
async def seo_generation_handler(message: Message) -> None:
    if message.text == "সাহায্য চাই":
        await message.answer("যেকোনো ভিডিওর টাইটেল লিখে পাঠান।")
        return

    wait_msg = await message.answer("⚡ Gemini চিন্তা করছে... (বেস্ট মডেল খোঁজা হচ্ছে)")
    
    # প্রম্পট তৈরি
    prompt = f"Act as a YouTube SEO Expert. Optimize title: '{message.text}'. Give 3 Titles, Description, and 15 Hashtags."
    
    # ফাংশন কল করা
    try:
        result = await call_gemini_api(prompt)
        await message.answer(f"✅ **রেজাল্ট:**\n\n{result}")
    except Exception as e:
        await message.answer(f"⚠️ **বট এরর:** {str(e)}")
    
    await wait_msg.delete()