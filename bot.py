import os
import google.generativeai as genai
from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart

router = Router()

# API Key সেটআপ
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

# লেটেস্ট এবং ফাস্ট মডেল
model = genai.GenerativeModel('gemini-1.5-flash')

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="সাহায্য চাই")]],
        resize_keyboard=True
    )
    welcome_msg = (
        f"👋 **স্বাগতম, {message.from_user.first_name}!**\n\n"
        "আমি Google Gemini (Flash) ⚡ দ্বারা চালিত আপনার SEO এক্সপার্ট।\n"
        "যেকোনো ভিডিওর **টাইটেল** পাঠান, আমি দিচ্ছি:\n"
        "✅ ৩টি অপ্টিমাইজড টাইটেল\n✅ এসইও ডেসক্রিপশন\n✅ ভাইরাল ট্যাগ"
    )
    await message.answer(welcome_msg, reply_markup=keyboard)

@router.message(F.text)
async def seo_generation_handler(message: Message) -> None:
    if message.text == "সাহায্য চাই":
        await message.answer("যেকোনো ভিডিওর টাইটেল লিখে পাঠান।")
        return

    wait_msg = await message.answer("⚡ Gemini চিন্তা করছে... একটু সময় দিন।")
    
    try:
        prompt = f"Act as a YouTube SEO Expert. Optimize title: '{message.text}'. Give 3 Titles, Description, and 15 Hashtags."
        
        # জেনারেট করা হচ্ছে
        response = await model.generate_content_async(prompt)
        
        if response.text:
            await message.answer(f"✅ **রেজাল্ট:**\n\n{response.text}")
        else:
            await message.answer("⚠️ উত্তর আসতে সমস্যা হয়েছে। আবার চেষ্টা করুন।")
            
        await wait_msg.delete()

    except Exception as e:
        await message.answer(f"⚠️ **সমস্যা হয়েছে:**\n{str(e)}\n\n(API Key টি Render-এ চেক করুন)")