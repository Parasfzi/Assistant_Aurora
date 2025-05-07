import speech_recognition as sr
import stop_flag
import time

def listen_for_stop():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        # Pause if no tasks are active to reduce CPU usage
        if not stop_flag.is_speaking:
            time.sleep(0.1)
            continue

        try:
            with mic as source:
                print("🎧 Listening for 'stop' command...")
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()

                if "stop" in command:
                    print("🛑 Stop command detected.")
                    stop_flag.stop_task = True
        except sr.UnknownValueError:
            continue
        except Exception as e:
            print("❌ Error in stop listener:", e)