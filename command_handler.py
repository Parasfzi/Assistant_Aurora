import webbrowser
import pyjokes
from smart_ai_module import ask_openrouter
import subprocess
from text_to_speech_module import speak
from web_search_module import search_google, get_weather
from timer_reminder_module import set_timer, set_reminder, cancel_timers, cancel_reminders
from email_module import send_email
from news_module import get_news
from custom_command_module import add_custom_command, edit_custom_command, delete_custom_command, execute_custom_command, list_custom_commands, load_custom_commands
from config import COMMANDS, CUSTOM_COMMAND_CATEGORIES
from stop_flag import stop_task
import logging
from speech_recognition_module import recognize_speech
import re

# Setup logging
logging.basicConfig(filename="aurora.log", level=logging.INFO)

def tell_joke():
    if stop_task: return speak("🚩 Task was cancelled.")
    joke = pyjokes.get_joke()
    speak(joke)
    logging.info("Told a joke")

def play_youtube_video(query):
    if stop_task: return speak("🚩 Task was cancelled.")
    speak(f"Playing {query} on YouTube")
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(url)
    logging.info(f"Played YouTube video: {query}")

def open_app(app_name):
    if stop_task: return speak("🚩 Task was cancelled.")
    apps = {
        "chrome": r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "notepad": "notepad.exe",
        "vscode": r"C:\\Users\\shikh\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
    }
    if app_name in apps:
        speak(f"Opening {app_name}")
        subprocess.Popen(apps[app_name])
        logging.info(f"Opened app: {app_name}")
    else:
        speak("Sorry, I don't know how to open that app.")
        logging.warning(f"Unknown app: {app_name}")

def handle_command(command, params=None):
    if not command:
        speak("Sorry, I didn't catch that.")
        return

    command = command.lower()
    print(f"Handling command: {command}")
    logging.info(f"Command received: {command}, params: {params}")

    if stop_task:
        speak("🚩 Task was cancelled.")
        return

    # Handle confirmation responses
    if command in ["yes", "sure", "okay", "confirm"] and hasattr(handle_command, "pending_action"):
        action = handle_command.pending_action
        logging.info(f"Processing confirmation for action: {action}")
        if action["type"] == "add_custom_command":
            add_custom_command(
                action["trigger"], action["actions"], action["category"], confirm=False
            )
            del handle_command.pending_action
            return
        elif action["type"] == "edit_custom_command":
            edit_custom_command(
                action["trigger"], action["new_actions"], confirm=False
            )
            del handle_command.pending_action
            return
        elif action["type"] == "delete_custom_command":
            delete_custom_command(action["trigger"], confirm=False)
            del handle_command.pending_action
            return
        elif action["type"] == "parameter_prompt":
            handle_command.pending_action["params"][action["param"]] = command
            execute_custom_command(action["trigger"], handle_command, action["params"])
            del handle_command.pending_action
            return

    if "search" in command:
        query = command.replace("search", "").strip()
        if query:
            search_google(query)
        else:
            speak("Please tell me what to search for.")

    elif "weather in" in command:
        city = command.split("weather in")[-1].strip()
        get_weather(city)

    elif "joke" in command:
        tell_joke()

    elif "play" in command and "on youtube" in command:
        query = command.replace("play", "").replace("on youtube", "").strip()
        play_youtube_video(query)

    elif "open" in command and not ("when i say" in command or "create a command" in command or "define command" in command or "edit command" in command):
        app_name = command.replace("open", "").strip()
        open_app(app_name)

    elif "set a timer for" in command:
        duration = command.replace("set a timer for", "").strip()
        logging.info(f"Setting timer with duration: {duration}")
        set_timer(duration)

    elif "remind me to" in command:
        parts = command.replace("remind me to", "").strip().split(" at ")
        if len(parts) == 2:
            message, time_str = parts
            set_reminder(message.strip(), time_str.strip())
        else:
            speak("Please specify a message and time, like 'remind me to call John at 3 PM'.")

    elif "stop timer" in command or "cancel timer" in command:
        cancel_timers()

    elif "stop reminder" in command or "cancel reminder" in command:
        cancel_reminders()

    elif "send an email to" in command:
        parts = command.replace("send an email to", "").strip().split(" about ")
        if len(parts) == 2:
            recipient, subject = parts
            recipient = recipient.strip().replace(" ", "").lower() + "@gmail.com"
            send_email(recipient, subject.strip(), f"Message from Aurora: {subject.strip()}")
        else:
            speak("Please specify a recipient and subject, like 'send an email to Jane about the meeting'.")

    elif "news about" in command or "tell me the news about" in command:
        query = command.replace("news about", "").replace("tell me the news about", "").strip()
        if query:
            get_news(query)
        else:
            speak("Please specify a topic for the news, like 'news about AI'.")

    elif "latest news" in command or "tell me the latest news" in command:
        get_news()

    elif any(phrase in command for phrase in ["when i say", "create a command", "define command"]):
        trigger = None
        actions = []
        category = "general"
        
        # Handle variations in phrasing
        if "when i say" in command:
            parts = command.split("when i say", 1)[-1].split("do the following", 1)
            if len(parts) != 2:
                parts = command.split("when i say", 1)[-1].split("to the following", 1)
            if len(parts) == 2:
                trigger = parts[0].strip()
                actions_part = parts[1].strip()
        elif "create a command" in command:
            parts = command.split("create a command", 1)[-1].split("to do", 1)
            if len(parts) == 2:
                trigger = parts[0].strip()
                actions_part = parts[1].strip()
        elif "define command" in command:
            parts = command.split("define command", 1)[-1].split("to do", 1)
            if len(parts) == 2:
                trigger = parts[0].strip()
                actions_part = parts[1].strip()
        else:
            speak("Please specify a trigger and actions, like 'when I say study mode do the following open VS Code and play focus playlist'.")
            return

        if " in " in actions_part:
            parts = actions_part.split(" in ")
            actions_part = parts[0].strip()
            category = parts[1].strip().split(" category")[0].strip()

        if actions_part:
            actions = [a.strip() for a in actions_part.split(" and ") if a.strip()]

        logging.info(f"Parsed custom command: trigger={trigger}, actions={actions}, category={category}")
        if trigger and actions:
            result = add_custom_command(trigger, actions, category, confirm=True)
            if result:
                handle_command.pending_action = {
                    "type": "add_custom_command",
                    "trigger": result["trigger"],
                    "actions": result["actions"],
                    "category": result["category"]
                }
        else:
            speak("Please specify a trigger and actions, like 'when I say study mode do the following open VS Code and play focus playlist'.")

    elif "edit command" in command:
        parts = command.split("edit command", 1)[-1].split("to add", 1)
        if len(parts) == 2:
            trigger = parts[0].strip()
            actions_part = parts[1].strip()
            actions = [a.strip() for a in actions_part.split(" and ") if a.strip()]
            logging.info(f"Parsed edit command: trigger={trigger}, actions={actions}")
            if trigger and actions:
                result = edit_custom_command(trigger, actions, confirm=True)
                if result:
                    handle_command.pending_action = {
                        "type": "edit_custom_command",
                        "trigger": result["trigger"],
                        "new_actions": result["new_actions"]
                    }
            else:
                speak("Please specify a trigger and actions to add, like 'edit command morning routine to add open notepad'.")
        else:
            speak("Please specify a trigger and actions to add, like 'edit command morning routine to add open notepad'.")

    elif "list my custom commands" in command or "list custom commands" in command:
        category = None
        if " in " in command:
            category = command.split(" in ")[-1].strip().split(" category")[0]
        list_custom_commands(category)

    elif "delete custom command" in command:
        trigger = command.replace("delete custom command", "").strip()
        if trigger:
            result = delete_custom_command(trigger, confirm=True)
            if result:
                handle_command.pending_action = {
                    "type": "delete_custom_command",
                    "trigger": result["trigger"]
                }
        else:
            speak("Please specify the command to delete, like 'delete custom command study mode'.")

    elif command in load_custom_commands():
        # Check for parameterized commands
        commands = load_custom_commands()
        params = params or {}
        logging.info(f"Executing custom command: {command}, params={params}")
        for action in commands[command]["actions"]:
            placeholders = re.findall(r"\{([a-zA-Z0-9_]+)\}", action)
            if placeholders:
                for param in placeholders:
                    if param not in params:
                        speak(f"What's the {param} for {action}?")
                        handle_command.pending_action = {
                            "type": "parameter_prompt",
                            "trigger": command,
                            "param": param,
                            "params": params
                        }
                        return
        execute_custom_command(command, handle_command, params)

    elif command in COMMANDS:
        if stop_task: return speak("🚩 Task was cancelled.")
        speak(COMMANDS[command])
        logging.info(f"Predefined command: {command}")

    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        logging.info("Exiting Aurora")
        exit()

    else:
        ai_response = ask_openrouter(command)
        if ai_response:
            speak(ai_response)
            logging.info(f"AI response: {ai_response}")
        else:
            speak("Sorry, I didn't understand that command.")
            logging.warning(f"Unrecognized command: {command}")