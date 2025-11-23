import redis
import os

# Redis connection URL (Render / Railway / Local সব জায়গায় কাজ করবে)
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Redis Client তৈরি
r = redis.from_url(redis_url, decode_responses=True)

# ---------- Chat ID Functions ----------

def save_user_chat_id(user_id, chat_id):
    """
    Save user's chat_id in Redis.
    Key: user:{user_id}:chat_id
    """
    r.set(f"user:{user_id}:chat_id", chat_id)


def get_user_chat_id(user_id):
    """
    Retrieve user's chat_id from Redis.
    """
    return r.get(f"user:{user_id}:chat_id")


def delete_user_chat_id(user_id):
    """
    Delete user's chat_id from Redis.
    """
    r.delete(f"user:{user_id}:chat_id")
