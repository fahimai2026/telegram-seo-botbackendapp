# backend/app/ai_client.py
import json
import openai
from config import settings
from tenacity import retry, wait_exponential, stop_after_attempt

openai.api_key = settings.OPENAI_API_KEY

SYSTEM_PROMPT = """
You are an expert YouTube SEO copywriter.
Given an input video title, produce JSON with fields:
- title (<=70 chars)
- description (2-3 lines)
- hashtags (array of 12 tags)
Return JSON only.
"""

@retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3))
def generate_seo(title: str, lang: str = "bn", tone: str = "energetic", variations: int = 1):
    prompt = f"Input Title: {title}\nLanguage: {lang}\nTone: {tone}\nReturn JSON only."
    resp = openai.ChatCompletion.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400,
        temperature=0.7,
        n=variations
    )

    outputs = []
    for choice in resp.choices:
        content = choice.message.get("content", "")
        try:
            data = json.loads(content)
        except Exception:
            import re
            m = re.search(r'(\{.*\})', content, re.S)
            if m:
                data = json.loads(m.group(1))
            else:
                data = {"title": content}
        outputs.append(data)
    return outputs
