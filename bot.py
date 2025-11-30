import aiohttp
from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart

router = Router()

# 👇 আপনার দেওয়া নতুন API KEY টি এখানে সরাসরি বসানো হয়েছে 👇
DIRECT_API_KEY = "AIzaSyBV8Q8w98zuOk0BqttODATsJMtm4kwQN_o"

async def call_gemini_api(prompt):
    # সরাসরি gemini-1.5-flash মডেলে হিট করা হচ্ছে
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={DIRECT_API_KEY}"
    
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
                except KeyError:
                    return "⚠️ উত্তর সাজাতে সমস্যা হয়েছে।"
            else:
                error_text = await response.text()
                return f"⚠️ Google Error ({response.status}): {error_text}"

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="সাহায্য চাই")]], resize_keyboard=True)
    await message.answer(f"স্বাগতম {message.from_user.first_name}! (Final Mode). যেকোনো ভিডিওর টাইটেল পাঠান।", reply_markup=kb)

@router.message(F.text)
async def seo_handler(message: Message) -> None:
    if message.text == "সাহায্য চাই":
        await message.answer("ভিডিওর টাইটেল দিন।")
        return

    msg = await message.answer("⚡ কাজ করছি... দেখা যাক কী হয়!")
    
    # এসইও প্রম্পট
    seo_prompt = f"Act as a YouTube SEO Expert. Optimize title: '{message.text}'. Give 3 Titles, Description, and 15 Hashtags."
    
    res = await call_gemini_api(seo_prompt)
    
    await message.answer(f"✅ **রেজাল্ট:**\n\n{res}")
    await msg.delete()