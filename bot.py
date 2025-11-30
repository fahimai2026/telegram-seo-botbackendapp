import os
import aiohttp
from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart

router = Router()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

async def call_gemini_api(prompt):
    if not GOOGLE_API_KEY:
        return "⚠️ API Key নেই! Render চেক করুন।"

    # সরাসরি gemini-1.5-flash মডেলে হিট করা হচ্ছে
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                return data['candidates'][0]['content']['parts'][0]['text']
            else:
                return f"⚠️ Google Error: {response.status}"

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="সাহায্য চাই")]], resize_keyboard=True)
    await message.answer(f"স্বাগতম {message.from_user.first_name}! আমি রেডি। যেকোনো ভিডিওর টাইটেল পাঠান।", reply_markup=kb)

@router.message(F.text)
async def seo_handler(message: Message) -> None:
    if message.text == "সাহায্য চাই":
        await message.answer("ভিডিওর টাইটেল দিন।")
        return

    msg = await message.answer("⚡ কাজ করছি...")
    res = await call_gemini_api(f"Act as YouTube SEO Expert. Optimize: '{message.text}'. Give Titles, Description, Tags.")
    await message.answer(f"✅ **রেজাল্ট:**\n\n{res}")
    await msg.delete()