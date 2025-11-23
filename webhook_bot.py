import os
from flask import Flask, request, jsonify
import telebot
from db import save_user_chat_id, get_user_chat_id  # আমরা db.py থেকে ব্যবহার করব

# Load environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def telegram_webhook():
    update = request.get_json()

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        # ইউজারের chat_id ডাটাবেজে সেভ করা হচ্ছে
        save_user_chat_id(chat_id)

        if text == "/start":
            bot.send_message(
                chat_id,
                "👋 Welcome! Your chat has been connected.\n"
                "✅ From now you’ll receive all updates & notifications here."
            )
        else:
            bot.send_message(chat_id, f"📩 You said: {text}")

    return jsonify({"ok": True})

# একটা হেল্পার ফাংশন — যেকোনো জায়গা থেকে নোটিফিকেশন পাঠানোর জন্য
def send_notification(user_id, message):
    chat_id = get_user_chat_id(user_id)
    if chat_id:
        bot.send_message(chat_id, message)
    else:
        print(f"No chat_id found for user {user_id}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
