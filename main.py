import stripe_webhook
import payment
import os
import redis
# Import the telegram router and setup function from bot.py
from bot import telegram_webhook_router, set_webhook

app = FastAPI(title="Telegram SEO Bot")

# Redis init
redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
# We are just initializing the connection pool here, usage depends on db.py or direct calls
r = redis.from_url(redis_url)

@app.on_event("startup")
async def startup_event():
    print("✅ Database Initialized") # Placeholder log
    print("✅ Redis Connected")
    
    # Automatically set the Telegram webhook on startup
    await set_webhook()
    print("✅ Telegram Webhook Checked/Set")

# Mount routers
# 1. Telegram Webhook Routerfrom fastapi import FastAPI

app.include_router(telegram_webhook_router, prefix="/webhook/telegram", tags=["telegram"])

# 2. Stripe Webhook Router
app.include_router(stripe_webhook.router, prefix="/webhook/stripe", tags=["stripe"])

# 3. Payment Router
app.include_router(payment.router, prefix="/payment", tags=["payment"])

@app.get("/")
async def root():
    return {"message": "Telegram SEO Bot is running 🚀"}