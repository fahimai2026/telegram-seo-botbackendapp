import os
import google.generativeai as genai
from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart

# ১. রাউটার তৈরি (main.py এর সাথে কানেক্ট করার জন্য)
router = Router()

# ২. Gemini কনফিগারেশন (Render Environment থেকে Key নেবে)
# যদি Key না পায়, তবে এরর দেবে না, কিন্তু কাজ করবে না। তাই Render-এ Key থাকা জরুরি।
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    print("⚠️ Warning: GEMINI_API_KEY not found in environment variables!")

# মডেল নির্বাচন (gemini-1.5-flash ফ্রি এবং দ্রুততম)
model = genai.GenerativeModel('gemini-1.5-flash')

# ৩. স্টার্ট (/start) কমান্ডের হ্যান্ডলার
@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    # একটি বাটন তৈরি
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="সাহায্য চাই")]
        ],
        resize_keyboard=True
    )
    
    welcome_msg = (
        f"👋 **স্বাগতম, {message.from_user.first_name}!**\n\n"
        "আমি Google Gemini ⚡ দ্বারা চালিত আপনার SEO এক্সপার্ট।\n"
        "যেকোনো ভিডিওর **টাইটেল (Title)** আমাকে পাঠান, আমি ফ্রিতে সেটির জন্য:\n\n"
        "✅ ৩টি অপ্টিমাইজড টাইটেল\n"
        "✅ এসইও ফ্রেন্ডলি ডেসক্রিপশন\n"
        "✅ ১৫টি ভাইরাল ট্যাগ\n\n"
        "তৈরি করে দেব। এখনই ট্রাই করুন! 👇"
    )
    await message.answer(welcome_msg, reply_markup=keyboard)

# ৪. SEO লজিক হ্যান্ডলার (যেকোনো টেক্সট মেসেজ এর জন্য)
@router.message(F.text)
async def seo_generation_handler(message: Message) -> None:
    # বাটন চাপলে সাধারণ উত্তর
    if message.text == "সাহায্য চাই":
        await message.answer("যেকোনো ইউটিউব ভিডিওর টাইটেল আমাকে লিখে পাঠান। আমি বাকিটা করে দেব।")
        return

    # ব্যবহারকারীকে অপেক্ষা করতে বলা
    wait_msg = await message.answer("⚡ Gemini আপনার টাইটেলটি বিশ্লেষণ করছে... একটু অপেক্ষা করুন।")
    
    user_title = message.text

    # Gemini-এর জন্য প্রম্পট তৈরি
    prompt = (
        f"Act as a professional YouTube SEO Expert. "
        f"Here is a video title: '{user_title}'.\n\n"
        "Please provide the following outputs:\n"
        "1. **3 High CTR Optimized Titles** (Mix of Bangla and English if the input is Bengali, otherwise English).\n"
        "2. **A Short SEO Description** (2-3 sentences including keywords).\n"
        "3. **15 Viral Hashtags** (Comma separated).\n\n"
        "Use emojis to make it look attractive."
    )

    try:
        # Gemini-তে রিকোয়েস্ট পাঠানো (Async)
        response = await model.generate_content_async(prompt)
        
        # রেসপন্স টেক্সট বের করা
        if response.text:
            seo_content = response.text
            # ব্যবহারকারীকে রেজাল্ট পাঠানো
            await message.answer(f"✅ **আপনার SEO রেজাল্ট:**\n\n{seo_content}")
        else:
            await message.answer("⚠️ দুঃখিত, কোনো উত্তর পাওয়া যায়নি। আবার চেষ্টা করুন।")
        
        # ওয়েটিং মেসেজটি ডিলিট করা
        await wait_msg.delete()

    except Exception as e:
        # এরর হ্যান্ডলিং
        error_msg = f"⚠️ দুঃখিত, একটি সমস্যা হয়েছে।\nError: {str(e)}\n\nদয়া করে Render-এ আপনার GEMINI_API_KEY চেক করুন।"
        await message.answer(error_msg)