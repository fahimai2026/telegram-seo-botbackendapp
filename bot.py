from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

# একটি রাউটার তৈরি করুন
router = Router()

# ১. স্টার্ট (/start) কমান্ডের হ্যান্ডলার
@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    print(f"Start command received from {message.from_user.id}") # লগে দেখার জন্য
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="আমার সম্পর্কে")],
            [KeyboardButton(text="সাহায্য চাই")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(f"স্বাগতম {message.from_user.first_name}! আমি কাজ করছি।", reply_markup=keyboard)

# ২. "আমার সম্পর্কে" টেক্সট মেসেজের হ্যান্ডলার
@router.message(F.text == "আমার সম্পর্কে")
async def about_handler(message: Message) -> None:
    await message.answer("আমি FastAPI এবং Aiogram দিয়ে তৈরি একটি বট।")

# ৩. ইকো হ্যান্ডলার
@router.message()
async def echo_handler(message: Message) -> None:
    await message.answer("আমি বুঝতে পারিনি। দয়া করে /start চাপুন।")