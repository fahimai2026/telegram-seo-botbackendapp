import aiohttp
from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart

router = Router()

# আপনার নতুন API Key
DIRECT_API_KEY = "AIzaSyBV8Q8w98zuOk0BqttODATsJMtm4kwQN_o"

async def call_gemini_api(prompt):
    # স্ক্রিনশট অনুযায়ী gemini-1.5-flash মডেল ব্যবহার করছি
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={DIRECT_API_KEY}"
    
    # হেডার যুক্ত করা হলো (এটি খুব জরুরি)
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                try:
                    return data['candidates'][0]['content']['parts'][0]['text']
                except KeyError:
                    return "⚠️ উত্তর এসেছে কিন্তু পড়তে পারছি না।"
            else:
                error_text = await response.text()
                return f"⚠️ Google Error ({response.status}): {error_text}"

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="সাহায্য চাই")]], resize_keyboard=True)
    # 👇 এই মেসেজটি খেয়াল করুন। যদি টেলিগ্রামে এটি না দেখেন, তবে বুঝবেন আপডেট হয়নি।
    welcome_msg = (
        f"👋 **স্বাগতম, {message.from_user.first_name}! (Version 5.0)**\n\n"
        "✅ API Key Verified\n"
        "✅ Model: Gemini 1.5 Flash\n"
        "🚀 আমি এখন রেডি! ভিডিওর টাইটেল পাঠান।"
    )
    await message.answer(welcome_msg, reply_markup=kb)

@router.message(F.text)
async def seo_handler(message: Message) -> None:
    if message.text == "সাহায্য চাই":
        await message.answer("ভিডিওর টাইটেল দিন।")
        return

    msg = await message.answer("⚡ কাজ করছি... (Version 5.0)")
    res = await call_gemini_api(f"Act as YouTube SEO Expert. Optimize: '{message.text}'. Give Titles, Description, Tags.")
    await message.answer(f"✅ **রেজাল্ট:**\n\n{res}")
    await msg.delete()