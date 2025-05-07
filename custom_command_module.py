import json
import os
import shutil
import re
from text_to_speech_module import speak
from config import CUSTOM_COMMAND_CATEGORIES
import logging

# Setup logging
logging.basicConfig(filename="aurora.log", level=logging.INFO)

# File to store custom commands
CUSTOM_COMMANDS_FILE = "custom_commands.json"
BACKUP_COMMANDS_FILE = "custom_commands_backup.json"

# Valid commands for validation (based on command_handler capabilities)
VALID_ACTIONS = [
    "search", "weather in", "joke", "play", "open", "set a timer for",
    "remind me to", "send an email to", "tell me the latest news", "news about", "exit", "quit"
]

def load_custom_commands():
    """Load custom commands from JSON file."""
    if os.path.exists(CUSTOM_COMMANDS_FILE):
        try:
            with open(CUSTOM_COMMANDS_FILE, "r") as f:
                return json.load(f)
        except:
            logging.error(f"Failed to load {CUSTOM_COMMANDS_FILE}. Attempting backup.")
            if os.path.exists(BACKUP_COMMANDS_FILE):
                try:
                    with open(BACKUP_COMMANDS_FILE, "r") as f:
                        return json.load(f)
                except:
                    logging.error(f"Failed to load backup {BACKUP_COMMANDS_FILE}.")
                    return {}
            return {}
    return {}

def save_custom_commands(commands):
    """Save custom commands to JSON file with backup."""
    if os.path.exists(CUSTOM_COMMANDS_FILE):
        shutil.copy(CUSTOM_COMMANDS_FILE, BACKUP_COMMANDS_FILE)
        logging.info("Created backup of custom commands")

    try:
        with open(CUSTOM_COMMANDS_FILE, "w") as f:
            json.dump(commands, f, indent=4)
        logging.info("Saved custom commands")
    except Exception as e:
        logging.error(f"Failed to save custom commands: {e}")
        speak("Error saving custom commands.")

def normalize_timer_action(action):
    """Normalize timer actions (e.g., 'set a timer for ten' → 'set a timer for 10 minutes')."""
    logging.info(f"Normalizing action: {action}")
    if action.startswith("set a timer for"):
        duration = action.replace("set a timer for", "").strip()
        number_map = {
            "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
            "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10"
        }
        if duration in number_map:
            normalized = f"set a timer for {number_map[duration]} minutes"
            logging.info(f"Normalized timer: {action} → {normalized}")
            return normalized
        elif duration.isdigit():
            normalized = f"set a timer for {duration} minutes"
            logging.info(f"Normalized timer: {action} → {normalized}")
            return normalized
        else:
            parts = duration.split()
            if len(parts) >= 2 and (parts[0].isdigit() or parts[0] in number_map) and "minute" in parts[1].lower():
                if parts[0] in number_map:
                    normalized = f"set a timer for {number_map[parts[0]]} minutes"
                    logging.info(f"Normalized timer: {action} → {normalized}")
                    return normalized
                return action  # Already in correct format
            logging.warning(f"Invalid timer duration: {duration}")
            speak(f"Invalid timer duration: {duration}")
            return None
    return action

def validate_action(action):
    """Check if an action is a valid Aurora command, including parameterized actions."""
    action = action.lower().strip()
    logging.info(f"Validating action: {action}")
    
    # Check timer actions (expect normalized format: 'set a timer for X minutes')
    if action.startswith("set a timer for"):
        duration = action.replace("set a timer for", "").strip()
        parts = duration.split()
        if len(parts) >= 2 and parts[0].isdigit() and "minute" in parts[1].lower():
            logging.info(f"Valid timer action: {action}")
            return True
        logging.warning(f"Invalid timer format: {action}")
        speak(f"Invalid timer format: {action}")
        return False
    
    # Check news actions
    if action == "tell me the latest news" or action.startswith("news about"):
        logging.info(f"Valid news action: {action}")
        return True
    
    # Handle parameterized actions (e.g., "search {query}")
    if re.match(r".*\{[a-zA-Z0-9_]+\}.*", action):
        base_action = re.sub(r"\{[a-zA-Z0-9_]+\}", "", action).strip()
        for valid in VALID_ACTIONS:
            if base_action.startswith(valid):
                logging.info(f"Valid parameterized action: {action}")
                return True
    
    # Check other valid actions
    for valid in VALID_ACTIONS:
        if action.startswith(valid) or action in load_custom_commands():
            logging.info(f"Valid action: {action}")
            return True
    
    logging.warning(f"Action validation failed: {action}")
    speak(f"Invalid action: {action}")
    return False

def add_custom_command(trigger, actions, category="general", confirm=False):
    """Add a custom command with a trigger phrase, actions, and category."""
    trigger = trigger.lower().strip()
    if not trigger:
        speak("Please provide a valid trigger phrase.")
        return False

    # Validate category
    category = category.lower()
    if category not in CUSTOM_COMMAND_CATEGORIES:
        speak(f"Invalid category. Choose from: {', '.join(CUSTOM_COMMAND_CATEGORIES)}.")
        return False

    # Normalize and validate actions
    valid_actions = []
    for action in actions:
        normalized_action = normalize_timer_action(action)
        if normalized_action is None:
            logging.warning(f"Skipped invalid action: {action}")
            continue
        if validate_action(normalized_action):
            valid_actions.append(normalized_action)
            logging.info(f"Added valid action: {normalized_action}")
        else:
            logging.warning(f"Invalid action after normalization: {normalized_action}")
    
    if not valid_actions:
        speak("No valid actions provided. Command not created.")
        return False

    if confirm:
        speak(f"Please confirm: Create command '{trigger}' with actions {', '.join(valid_actions)} in category '{category}'? Say 'yes', 'sure', 'okay', or 'confirm'.")
        return {"trigger": trigger, "actions": valid_actions, "category": category}

    commands = load_custom_commands()
    commands[trigger] = {
        "actions": valid_actions,
        "category": category
    }
    save_custom_commands(commands)
    speak(f"Custom command '{trigger}' added in category '{category}'.")
    logging.info(f"Custom command added: {trigger}, category: {category}, actions: {valid_actions}")
    return True

def edit_custom_command(trigger, new_actions, confirm=False):
    """Edit an existing custom command by adding new actions."""
    trigger = trigger.lower().strip()
    commands = load_custom_commands()
    
    if trigger not in commands:
        speak(f"No custom command found for '{trigger}'.")
        return False

    # Normalize and validate new actions
    valid_actions = []
    for action in new_actions:
        normalized_action = normalize_timer_action(action)
        if normalized_action is None:
            logging.warning(f"Skipped invalid action: {action}")
            continue
        if validate_action(normalized_action):
            valid_actions.append(normalized_action)
            logging.info(f"Added valid new action: {normalized_action}")
        else:
            logging.warning(f"Invalid action after normalization: {normalized_action}")

    if not valid_actions:
        speak("No valid actions provided. Command not edited.")
        return False

    if confirm:
        speak(f"Please confirm: Add actions {', '.join(valid_actions)} to command '{trigger}'? Say 'yes', 'sure', 'okay', or 'confirm'.")
        return {"trigger": trigger, "new_actions": valid_actions}

    commands[trigger]["actions"].extend(valid_actions)
    save_custom_commands(commands)
    speak(f"Custom command '{trigger}' updated with new actions.")
    logging.info(f"Custom command edited: {trigger}, added actions: {valid_actions}")
    return True

def delete_custom_command(trigger, confirm=False):
    """Delete a custom command."""
    trigger = trigger.lower().strip()
    commands = load_custom_commands()
    
    if trigger not in commands:
        speak(f"No custom command found for '{trigger}'.")
        return False

    if confirm:
        speak(f"Please confirm: Delete command '{trigger}'? Say 'yes', 'sure', 'okay', or 'confirm'.")
        return {"trigger": trigger}

    del commands[trigger]
    save_custom_commands(commands)
    speak(f"Custom command '{trigger}' deleted.")
    logging.info(f"Custom command deleted: {trigger}")
    return True

def list_custom_commands(category=None):
    """List all custom commands, optionally filtered by category."""
    commands = load_custom_commands()
    if not commands:
        speak("No custom commands defined.")
        return

    if category:
        category = category.lower()
        if category not in CUSTOM_COMMAND_CATEGORIES:
            speak(f"Invalid category. Choose from: {', '.join(CUSTOM_COMMAND_CATEGORIES)}.")
            return
        filtered = {k: v for k, v in commands.items() if v["category"] == category}
        if not filtered:
            speak(f"No custom commands in category '{category}'.")
            return
        speak(f"Custom commands in category '{category}':")
        for trigger, data in filtered.items():
            speak(f"Trigger: {trigger}, Actions: {', '.join(data['actions'])}")
        logging.info(f"Listed custom commands in category: {category}")
    else:
        speak("All custom commands:")
        for trigger, data in commands.items():
            speak(f"Trigger: {trigger}, Category: {data['category']}, Actions: {', '.join(data['actions'])}")
        logging.info("Listed all custom commands")

def execute_custom_command(trigger, handle_command_func, params=None):
    """Execute a custom command, substituting parameters if provided."""
    commands = load_custom_commands()
    trigger = trigger.lower().strip()
    if trigger not in commands:
        speak(f"No custom command found for '{trigger}'.")
        logging.warning(f"Unknown custom command: {trigger}")
        return

    for action in commands[trigger]["actions"]:
        logging.info(f"Executing action: {action}")
        # Substitute parameters in actions
        if params and re.search(r"\{[a-zA-Z0-9_]+\}", action):
            formatted_action = action
            for param, value in params.items():
                formatted_action = formatted_action.replace(f"{{{param}}}", value)
            logging.info(f"Formatted action with params: {formatted_action}")
            handle_command_func(formatted_action)
        else:
            handle_command_func(action)
    logging.info(f"Executed custom command: {trigger}, params: {params}")