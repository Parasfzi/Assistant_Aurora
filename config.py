# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

WAKE_WORDS = ["aurora", "arora", "hey aurora", "hello aurora", "ah rawat", "rawat", "i rawat", "oi aurora", "yo aurora", "arora", "an aura"]
TTS_ENGINE = "sapi5"

# API keys from environment variables
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# Predefined categories for custom commands
CUSTOM_COMMAND_CATEGORIES = ["productivity", "entertainment", "general"]
WELCOME_MESSAGE = "Hello, I’m Aurora, your personal assistant. How can I help you?"
COMMANDS = {
    "how are you": "I'm doing great, Paras!",
    "who are you": "I'm Aurora, your AI assistant.",
    "what can you do": "I can search, tell weather, open apps, play YouTube videos, set timers, send emails, manage custom commands, and more!"
}