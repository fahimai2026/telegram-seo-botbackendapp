import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # আপনার .env ফাইলে যা যা আছে, সেই নামগুলো এখানে থাকতে হবে
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
    STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
    # যদি আরও কোনো ভেরিয়েবল থাকে (যেমন DB_URL), তা এখানে যোগ করুন
    
settings = Settings()