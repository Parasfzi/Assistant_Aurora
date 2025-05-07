import threading
import time
import datetime
from text_to_speech_module import speak
import stop_flag
import logging

# Setup logging
logging.basicConfig(filename="aurora.log", level=logging.INFO)

# Store active timers and reminders
timers = []
reminders = []

def timer_thread(duration, label="timer"):
    """Run a timer for the specified duration (in seconds)."""
    start_time = time.time()
    while time.time() - start_time < duration:
        if stop_flag.stop_task:
            speak(f"🛑 {label} cancelled.")
            logging.info(f"Timer cancelled: {label}")
            return
        time.sleep(1)
    if not stop_flag.stop_task:
        speak(f"⏰ {label} is up!")
        logging.info(f"Timer completed: {label}")

def reminder_thread(message, target_time, label="reminder"):
    """Check until the target time is reached for a reminder."""
    while datetime.datetime.now() < target_time:
        if stop_flag.stop_task:
            speak(f"🛑 {label} cancelled.")
            logging.info(f"Reminder cancelled: {label}")
            return
        time.sleep(10)  # Check every 10 seconds
    if not stop_flag.stop_task:
        speak(f"⏰ Reminder: {message}")
        logging.info(f"Reminder triggered: {message}")

def set_timer(duration_str):
    """Parse and start a timer (e.g., '5 minutes', 'ten', '10 minutes')."""
    try:
        duration_str = duration_str.strip().lower()
        logging.info(f"Setting timer with duration: {duration_str}")
        number_map = {
            "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
        }

        # Handle shorthand (e.g., "ten") or numeric inputs (e.g., "5")
        if duration_str in number_map:
            value = number_map[duration_str]
            duration = value * 60  # Assume minutes
            unit = "minutes"
        elif duration_str.isdigit():
            value = int(duration_str)
            duration = value * 60  # Assume minutes
            unit = "minutes"
        else:
            # Handle explicit units (e.g., "5 minutes", "10 minutes")
            parts = duration_str.split()
            if not parts:
                speak("Please specify a duration, like '5 minutes' or 'ten'.")
                logging.error(f"Empty duration string: {duration_str}")
                return
            value_str = parts[0]
            unit = parts[1].lower() if len(parts) > 1 else "minutes"
            
            # Convert value_str to numeric
            if value_str in number_map:
                value = number_map[value_str]
            else:
                value = int(value_str)
                
            if "minute" in unit:
                duration = value * 60
            elif "second" in unit:
                duration = value
            else:
                speak("Please use 'minutes' or 'seconds'.")
                logging.error(f"Invalid unit in duration: {unit}")
                return

        timer_label = f"{value} {unit} timer"
        timer = threading.Thread(target=timer_thread, args=(duration, timer_label), daemon=True)
        timers.append(timer)
        timer.start()
        speak(f"Timer set for {value} {unit}.")
        logging.info(f"Timer set: {timer_label}")
    except (ValueError, IndexError) as e:
        speak("Sorry, I couldn't understand the duration.")
        logging.error(f"Timer parsing error: {duration_str}, Exception: {str(e)}")

def set_reminder(message, time_str):
    """Parse and start a reminder (e.g., 'call John at 3 PM')."""
    try:
        target_time = datetime.datetime.strptime(time_str, "%I %p")
        target_time = target_time.replace(
            year=datetime.datetime.now().year,
            month=datetime.datetime.now().month,
            day=datetime.datetime.now().day
        )
        if target_time < datetime.datetime.now():
            target_time += datetime.timedelta(days=1)  # Assume next day if time passed

        reminder_label = f"reminder for {message}"
        reminder = threading.Thread(
            target=reminder_thread, args=(message, target_time, reminder_label), daemon=True
        )
        reminders.append(reminder)
        reminder.start()
        speak(f"Reminder set for {message} at {time_str}.")
        logging.info(f"Reminder set: {message} at {time_str}")
    except ValueError:
        speak("Sorry, I couldn't understand the time. Use formats like '3 PM' or '14:30'.")
        logging.error(f"Invalid reminder time: {time_str}")

def cancel_timers():
    """Cancel all active timers."""
    if timers:
        stop_flag.stop_task = True
        time.sleep(0.1)  # Allow threads to catch stop flag
        stop_flag.stop_task = False
        timers.clear()
        speak("All timers cancelled.")
        logging.info("All timers cancelled")
    else:
        speak("No active timers to cancel.")

def cancel_reminders():
    """Cancel all active reminders."""
    if reminders:
        stop_flag.stop_task = True
        time.sleep(0.1)
        stop_flag.stop_task = False
        reminders.clear()
        speak("All reminders cancelled.")
        logging.info("All reminders cancelled")
    else:
        speak("No active reminders to cancel.")