# backend/app/payment.py
from fastapi import APIRouter, HTTPException
import stripe
import os
from config import settings

router = APIRouter()
stripe.api_key = settings.STRIPE_SECRET

@router.post("/create-checkout-session")
async def create_checkout_session(telegram_id: str):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[{
                "price": settings.STRIPE_PRICE_PRO,
                "quantity": 1,
            }],
            client_reference_id=telegram_id,
            success_url=f"https://your-domain.com/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"https://your-domain.com/cancel",
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating session: {e}")
