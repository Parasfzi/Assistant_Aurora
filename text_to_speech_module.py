import pyttsx3
import time
import stop_flag
import re
from config import TTS_ENGINE

engine = pyttsx3.init(TTS_ENGINE)
engine.setProperty("rate", 170)

# Try to use a female voice
voices = engine.getProperty("voices")
female_voice = next((v for v in voices if "female" in v.name.lower() or "zira" in v.name.lower()), None)
if female_voice:
    engine.setProperty("voice", female_voice.id)
else:
    print("⚠️ Female voice not found. Using default voice.")

def speak(text):
    """Speak text in natural phrases with stop word detection."""
    if not text or not text.strip():
        return

    print("🎤 Aurora:", text)
    stop_flag.is_speaking = True

    try:
        # Split into phrases/sentences
        sentences = re.split(r'(?<=[.!?…:]) +', text)

        for sentence in sentences:
            if stop_flag.stop_task:
                print("🛑 Speech interrupted mid-sentence.")
                engine.stop()
                break

            clean = sentence.strip()
            if clean:
                print(f"🗣️ Saying: {clean}")
                engine.say(clean)
                engine.runAndWait()
                time.sleep(0.05)  # natural pause

    finally:
        stop_flag.is_speaking = False