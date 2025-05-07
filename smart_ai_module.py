import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 🔐 OpenRouter API key from environment
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# 📁 File to store local cache
CACHE_FILE = "response_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)

def clean_response(text):
    if not text:
        return "I didn't understand that."
    lines = text.strip().splitlines()
    final_lines = []
    for line in lines:
        if len(final_lines) >= 6:
            break
        if line.strip().startswith("```"):
            continue
        final_lines.append(line.strip())
    return " ".join(final_lines)

def ask_openrouter(prompt):
    cache = load_cache()
    key = prompt.lower().strip()

    if key in cache:
        print("📦 Cached response used.")
        return cache[key]

    if not OPENROUTER_API_KEY:
        print("❌ OpenRouter API key missing.")
        return "API key not configured."

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "deepseek/deepseek-chat-v3-0324:free",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are Aurora, a smart, factual AI assistant. "
                        "If the user asks about a topic like weather, science, or general knowledge, "
                        "explain clearly and concisely. Do not make things up or change the subject."
                    )
                },
                {
                    "role": "user",
                    "content": f"User asked: '{prompt}'. Please explain briefly and accurately, staying on-topic."
                }
            ],
            "temperature": 0.7,
            "max_tokens": 300
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
            cleaned = clean_response(reply)
            cache[key] = cleaned
            save_cache(cache)
            return cleaned
        else:
            print("🔴 API Error:", response.status_code, response.text)
            return "Sorry, I couldn’t reach the AI server."

    except Exception as e:
        print("❌ OpenRouter error:", e)
        return "There was an error contacting OpenRouter."