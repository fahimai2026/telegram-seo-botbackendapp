import os
import aiohttp
from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart

router = Router()

# API Key পরিবেশ থেকে নেওয়া
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

# --- ডাইরেক্ট API কল ফাংশন (gemini-pro) ---
async def call_gemini_api(prompt):
    if not GOOGLE_API_KEY:
        return "⚠️ API Key পাওয়া যায়নি! Render-এ চেক করুন।"

    # এখানে মডেল নাম পরিবর্তন করে 'gemini-pro' করা হয়েছে
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GOOGLE_API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                try:
                    return data['candidates'][0]['content']['parts'][0]['text']
                except (KeyError, IndexError):
                    return "⚠️ উত্তর সাজাতে সমস্যা হয়েছে। আবার চেষ্টা করুন।"
            else:
                error_text = await response.text()
                return f"⚠️ Google Error ({response.status}): {error_text}"

# -------------------------------------------

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="সাহায্য চাই")]],
        resize_keyboard=True
    )
    welcome_msg = (
        f"👋 **স্বাগতম, {message.from_user.first_name}!**\n\n"
        "আমি Google Gemini (Pro) ⚡ দ্বারা চালিত আপনার SEO এক্সপার্ট।\n"
        "যেকোনো ভিডিওর **টাইটেল** পাঠান, আমি দিচ্ছি:\n"
        "✅ ৩টি অপ্টিমাইজড টাইটেল\n✅ এসইও ডেসক্রিপশন\n✅ ভাইরাল ট্যাগ"
    )
    await message.answer(welcome_msg, reply_markup=keyboard)

@router.message(F.text)
async def seo_generation_handler(message: Message) -> None:
    if message.text == "সাহায্য চাই":
        await message.answer("যেকোনো ভিডিওর টাইটেল লিখে পাঠান।")
        return

    wait_msg = await message.answer("⚡ Gemini চিন্তা করছে... (Direct Mode)")
    
    # প্রম্পট তৈরি
    prompt = f"Act as a YouTube SEO Expert. Optimize title: '{message.text}'. Give 3 Titles, Description, and 15 Hashtags."
    
    # ফাংশন কল করা
    try:
        result = await call_gemini_api(prompt)
        await message.answer(f"✅ **রেজাল্ট:**\n\n{result}")
    except Exception as e:
        await message.answer(f"⚠️ **বট এরর:** {str(e)}")
    
    await wait_msg.delete()