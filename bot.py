import os
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from openai import AsyncOpenAI

# রাউটার তৈরি
router = Router()

# OpenAI ক্লায়েন্ট সেটআপ (Render Environment থেকে Key নেবে)
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ১. স্টার্ট (/start) কমান্ডের হ্যান্ডলার
@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="সাহায্য চাই")]
        ],
        resize_keyboard=True
    )
    
    welcome_msg = (
        f"👋 **স্বাগতম, {message.from_user.first_name}!**\n\n"
        "আমি আপনার ভিডিও SEO এক্সপার্ট। 🚀\n"
        "যেকোনো ভিডিওর **টাইটেল (Title)** আমাকে পাঠান, আমি সেটির জন্য:\n"
        "✅ অপ্টিমাইজড টাইটেল\n"
        "✅ ডেসক্রিপশন\n"
        "✅ ভাইরাল ট্যাগস\n"
        "তৈরি করে দেব।"
    )
    await message.answer(welcome_msg, reply_markup=keyboard)

# ২. SEO লজিক হ্যান্ডলার (যেকোনো টেক্সট মেসেজ এর জন্য)
@router.message(F.text)
async def seo_generation_handler(message: Message) -> None:
    # ব্যবহারকারীকে অপেক্ষা করতে বলা
    wait_msg = await message.answer("🔍 আপনার টাইটেলটি বিশ্লেষণ করছি... একটু অপেক্ষা করুন।")
    
    user_title = message.text

    try:
        # OpenAI তে রিকোয়েস্ট পাঠানো
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo", # অথবা gpt-4o ব্যবহার করতে পারেন যদি এক্সেস থাকে
            messages=[
                {"role": "system", "content": "You are a professional YouTube SEO expert. The user will provide a video title. You must provide: 1. 3 Optimized Titles (High CTR). 2. A short SEO description (2-3 lines). 3. 15 Viral Hashtags."},
                {"role": "user", "content": f"Optimize this video title for YouTube: '{user_title}'"}
            ]
        )
        
        # রেসপন্স থেকে কন্টেন্ট বের করা
        seo_content = response.choices[0].message.content
        
        # ব্যবহারকারীকে পাঠানো
        await message.answer(f"✅ **SEO রেজাল্ট:**\n\n{seo_content}")
        
        # ওয়েটিং মেসেজটি ডিলিট করা (অপশনাল)
        await wait_msg.delete()

    except Exception as e:
        await message.answer(f"⚠️ দুঃখিত, একটি সমস্যা হয়েছে: {str(e)}\nদয়া করে আপনার API Key চেক করুন।")