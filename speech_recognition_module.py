import sounddevice as sd
import queue
import json
import vosk
import sys
import os
import logging

# Setup logging
logging.basicConfig(filename="aurora.log", level=logging.INFO)

# Audio queue for streaming mic data
q = queue.Queue()

# Check for VOSK model
MODEL_PATH = "vosk-model-en-hi"
if not os.path.exists(MODEL_PATH):
    print(f"❌ VOSK model not found at '{MODEL_PATH}'. Please download it.")
    logging.error(f"VOSK model not found at '{MODEL_PATH}'")
    sys.exit(1)

# Load the VOSK model
try:
    model = vosk.Model(MODEL_PATH)
except Exception as e:
    print("❌ Could not load VOSK model:", e)
    logging.error(f"Could not load VOSK model: {e}")
    sys.exit(1)

# Callback for audio data
def callback(indata, frames, time, status):
    if status:
        print("⚠️ Stream status:", status)
        logging.warning(f"Stream status: {status}")
    q.put(bytes(indata))

# Transcribes speech and returns it cleanly
def recognize_speech():
    print("🎧 Listening with VOSK...")
    logging.info("Started speech recognition")
    try:
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=callback):
            rec = vosk.KaldiRecognizer(model, 16000)

            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "").lower().strip()
                    logging.info(f"Recognized speech: {text}")
                    return text
    except Exception as e:
        print("❌ Microphone input error:", e)
        logging.error(f"Microphone input error: {e}")
        return ""