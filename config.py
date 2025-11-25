import os

class Settings:
    # Telegram
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_WEBHOOK_URL: str = os.getenv("TELEGRAM_WEBHOOK_URL")
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL")
    
    # Stripe
    STRIPE_SECRET: str = os.getenv("STRIPE_SECRET")
    STRIPE_PRICE_PRO: str = os.getenv("STRIPE_PRICE_PRO")
    STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET")

    # Database & Cache
    REDIS_URL: str = os.getenv("REDIS_URL")
    DB_PATH: str = os.getenv("DB_PATH", "seo_bot.db")
    
    # Limits
    FREE_LIMIT: int = int(os.getenv("FREE_LIMIT", 5))

settings = Settings()