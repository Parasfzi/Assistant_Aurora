import platform
import time
import stop_flag
import re

system = platform.system()

if system == "Windows":
    import pyttsx3
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
        """Speak text in natural phrases with stop word detection (Windows)."""
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


else:
    # Linux / Codespaces fallback: gTTS + playsound
    from gtts import gTTS
    import os
    from playsound import playsound

    def speak(text):
        """Speak text using gTTS (Linux fallback)."""
        if not text or not text.strip():
            return

        print("🎤 Aurora:", text)
        stop_flag.is_speaking = True

        try:
            tts = gTTS(text=text, lang="en")
            filename = "temp_audio.mp3"
            tts.save(filename)
            playsound(filename)
            os.remove(filename)
        except Exception as e:
            print(f"[TTS Error on Linux] {e}")
            print(text)  # fallback: just print
        finally:
            stop_flag.is_speaking = False
