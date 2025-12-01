import aiohttp
from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart

router = Router()

# আপনার নতুন API KEY
DIRECT_API_KEY = "AIzaSyBV8Q8w98zuOk0BqttODATsJMtm4kwQN_o"

# ১. অটোমেটিক সঠিক মডেল খুঁজে বের করার ফাংশন
async def get_best_available_model():
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={DIRECT_API_KEY}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                # লিস্ট থেকে gemini মডেল খোঁজা হচ্ছে
                for model in data.get('models', []):
                    name = model['name'] # যেমন: models/gemini-1.5-flash
                    methods = model.get('supportedGenerationMethods', [])
                    
                    # আমরা দেখব এই মডেলটি 'generateContent' সাপোর্ট করে কিনা
                    if 'generateContent' in methods and 'gemini' in name:
                        return name # প্রথম যে সচল মডেল পাবে, সেটাই রিটার্ন করবে
            return None

# ২. মেইন API কল ফাংশন
async def call_gemini_api(prompt):
    # আগে সঠিক মডেলটি খুঁজে বের করি
    model_name = await get_best_available_model()
    
    if not model_name:
        return "⚠️ সমস্যা: Render থেকে Google-এর কোনো মডেল লোড করা যাচ্ছে না। (IP Blocked or Key Issue)"

    # সেই মডেলটি ব্যবহার করে কল করা
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={DIRECT_API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
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
    welcome_msg = (
        f"👋 **স্বাগতম, {message.from_user.first_name}! (Version 6.0)**\n\n"
        "🤖 **Auto-Model Mode Activated**\n"
        "বট এখন নিজে থেকেই সচল মডেল খুঁজে নেবে।\n\n"
        "ভিডিওর টাইটেল পাঠান 👇"
    )
    await message.answer(welcome_msg, reply_markup=kb)

@router.message(F.text)
async def seo_handler(message: Message) -> None:
    if message.text == "সাহায্য চাই":
        await message.answer("ভিডিওর টাইটেল দিন।")
        return

    msg = await message.answer("⚡ সেরা মডেল খুঁজছি এবং কাজ করছি... (v6.0)")
    res = await call_gemini_api(f"Act as YouTube SEO Expert. Optimize: '{message.text}'. Give Titles, Description, Tags.")
    await message.answer(f"✅ **রেজাল্ট:**\n\n{res}")
    await msg.delete()