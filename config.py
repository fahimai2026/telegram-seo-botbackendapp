import os
from pydantic_settings import BaseSettings

# BaseSettings class automatically loads environment variables 
# from the system environment (which Render uses)
class Settings(BaseSettings):
    # Telegram
    TELEGRAM_TOKEN: str
    TELEGRAM_WEBHOOK_URL: str
    
    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str
    
    # Stripe
    STRIPE_SECRET: str
    STRIPE_PRICE_PRO: str
    STRIPE_WEBHOOK_SECRET: str

    # Database & Cache
    REDIS_URL: str
    DB_PATH: str = "seo_bot.db"
    
    # Limits
    FREE_LIMIT: int = 5
    
    class Config:
        # Pydantic-Settings-কে বলা হচ্ছে যেন শুধুমাত্র OS Environment থেকে ভ্যালু নেয়
        # এবং .env ফাইল লোড করার চেষ্টা না করে।
        env_file = None 
        env_file_encoding = 'utf-8'

settings = Settings()