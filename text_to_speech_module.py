import platform
import time
import stop_flag
import re

system_os = platform.system()

if system_os == "Windows":
    import pyttsx3
    from config import TTS_ENGINE

    engine = pyttsx3.init(TTS_ENGINE)
    engine.setProperty("rate", 170)

    voices = engine.getProperty("voices")
    female_voice = next((v for v in voices if "female" in v.name.lower() or "zira" in v.name.lower()), None)
    if female_voice:
        engine.setProperty("voice", female_voice.id)
    else:
        print("⚠️ Female voice not found. Using default voice.")

    def speak(text):
        """Speak text with pyttsx3 on Windows."""
        if not text or not text.strip():
            return

        print("🎤 Aurora:", text)
        stop_flag.is_speaking = True

        try:
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
                    time.sleep(0.05)
        finally:
            stop_flag.is_speaking = False

else:
    from gtts import gTTS
    import os
    import pygame

    def speak(text):
        """Speak text with gTTS + pygame on Linux/Mac (Codespaces)."""
        if not text or not text.strip():
            return

        print("🎤 Aurora:", text)
        stop_flag.is_speaking = True

        try:
            tts = gTTS(text=text, lang="en")
            filename = "temp_audio.mp3"
            tts.save(filename)

            pygame.mixer.init()
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                continue

            os.remove(filename)
        except Exception as e:
            print(f"[TTS Error on {system_os}] {e}")
            print(text)  # fallback
        finally:
            stop_flag.is_speaking = False
