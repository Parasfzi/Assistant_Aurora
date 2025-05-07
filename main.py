import threading
import time
from text_to_speech_module import speak
from speech_recognition_module import recognize_speech
from command_handler import handle_command
import stop_flag
from stop_listener import listen_for_stop
import logging

# Setup logging
logging.basicConfig(filename="aurora.log", level=logging.INFO)

# Wake word list
WAKE_WORDS = ["aurora", "arora", "hey aurora", "hello aurora", "ah rawat", "rawat", "i rawat", "oi aurora", "yo aurora", "arora", "an aura"]

print("🤖 Hello! I'm Aurora. How can I help you today?")
speak("Hello Paras")
logging.info("Aurora started")

time.sleep(2)
stop_flag.stop_task = False
stop_thread = threading.Thread(target=listen_for_stop, daemon=True)
stop_thread.start()

while True:
    try:
        print("🎤 Aura is Listening...")
        original_command = recognize_speech()

        if not original_command:
            print("🟡 No command recognized.")
            speak("Sorry, I didn't catch that.")
            continue

        print(f"🧠 Raw Transcript: {original_command}")
        logging.info(f"Raw transcript: {original_command}")

        command = original_command.lower().strip()

        # Check for wake word match
        matched = None
        for wake in WAKE_WORDS:
            if command.startswith(wake):
                matched = wake
                break

        if not matched:
            print("❌ Wake word not detected.")
            speak("Say 'Aurora' to activate me.")
            continue

        # Remove the matched wake word
        command = command.replace(matched, "", 1).strip()
        print(f"🗣️ You said: {command}")
        logging.info(f"Processed command: {command}")

        if stop_flag.stop_task:
            print("🛑 Stop flag was triggered before task.")
            speak("Okay, stopping that.")
            stop_flag.stop_task = False
            continue

        handle_command(command)
        stop_flag.stop_task = False

    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        speak("Goodbye Paras!")
        logging.info("Aurora stopped")
        break

    except Exception as e:
        print("❌ Error in main loop:", e)
        logging.error(f"Main loop error: {e}")
        speak("Something went wrong.")