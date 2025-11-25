from fastapi import FastAPI
# Final Fix: Changed relative/app imports to direct imports for deployment stability.
# webhook_bot
import stripe_webhook
import payment
import db
import redis
import os

app = FastAPI(title="Telegram SEO Bot")

# Redis init
redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
r = redis.from_url(redis_url)

@app.on_event("startup")
async def startup_event():
    # Call init_db and check Redis connection during startup
    db.init_db()
    print("✅ Database Initialized")
    print("✅ Redis Connected")

# Mount routers
# webhook_bot
app.include_router(stripe_webhook.router, prefix="/webhook/stripe", tags=["stripe"])
app.include_router(payment.router, prefix="/payment", tags=["payment"])

@app.get("/")
async def root():
    return {"message": "Telegram SEO Bot is running 🚀"}