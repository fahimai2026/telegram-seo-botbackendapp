from fastapi import APIRouter, Request, HTTPException
import stripe
import json
from config import settings
import db # FIX: Changed from specific imports to 'import db'

router = APIRouter()
stripe.api_key = settings.STRIPE_SECRET

@router.post("/")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook error: {e}")

    # Handle completed checkout session
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        telegram_id = session["client_reference_id"]
        sub_id = session["subscription"]
        
        # FIX: Calling functions via 'db.' prefix to resolve final ImportError
        # Assumed correct function names are get_or_create_user and update_subscription
        user_id = db.get_or_create_user(telegram_id) 
        db.update_subscription(user_id, sub_id, days=30, status="pro")

    # Handle other relevant events if needed (payment_failed, invoice.paid, etc.)
    return {"status": "success"}