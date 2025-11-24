from fastapi import FastAPI
# Corrected import path for flat structure (modules in the same directory)
from . import webhook_bot, stripe_webhook, payment, db
import redis
import os

app = FastAPI(title="Telegram SEO Bot")

# Redis init
redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
r = redis.from_url(redis_url)

@app.on_event("startup")
async def startup_event():
    db.init_db()
    print("✅ Database Initialized")
    print("✅ Redis Connected")

# Mount routers
app.include_router(webhook_bot.router, prefix="/webhook/telegram", tags=["telegram"])
app.include_router(stripe_webhook.router, prefix="/webhook/stripe", tags=["stripe"])
app.include_router(payment.router, prefix="/payment", tags=["payment"])

@app.get("/")
async def root():
    return {"message": "Telegram SEO Bot is running 🚀"}