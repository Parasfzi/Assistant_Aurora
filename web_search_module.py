import requests
import wikipedia
from text_to_speech_module import speak
from config import OPENWEATHER_API_KEY, SERPAPI_KEY
from smart_ai_module import ask_openrouter
import webbrowser
import stop_flag
import logging

# Setup logging
logging.basicConfig(filename="aurora.log", level=logging.INFO)

def search_google(query):
    if stop_flag.stop_task:
        speak("🛑 Task was cancelled.")
        return

    speak(f"Searching for {query}...")
    logging.info(f"Search query: {query}")

    if not SERPAPI_KEY:
        speak("Search API key is missing.")
        return

    try:
        url = f"https://serpapi.com/search?api_key={SERPAPI_KEY}&q={query.replace(' ', '+')}"
        response = requests.get(url).json()

        if "organic_results" not in response or not response["organic_results"]:
            speak("Sorry, I couldn't find anything useful.")
            return

        result = response["organic_results"][0]
        snippet = result.get("snippet", "No description available.")
        link = result.get("link", f"https://duckduckgo.com/?q={query.replace(' ', '+')}")

        if stop_flag.stop_task:
            speak("🛑 Task was cancelled.")
            return

        ai_prompt = f"Summarize or explain this:\n\n\"{snippet}\""
        summary = ask_openrouter(ai_prompt)
        webbrowser.open(link)

        if stop_flag.stop_task:
            speak("🛑 Task was cancelled.")
            return

        if summary:
            speak(summary)
            return summary
        else:
            speak("Here's what I found, but I couldn't summarize it.")
            speak(snippet)
            return snippet

    except Exception as e:
        print("Search error:", e)
        logging.error(f"Search error: {e}")
        speak("Something went wrong while searching.")
        return

def get_wikipedia_summary(topic):
    """Get summary from Wikipedia."""
    speak(f"Searching Wikipedia for {topic}...")
    logging.info(f"Wikipedia query: {topic}")
    try:
        summary = wikipedia.summary(topic, sentences=2)
        speak(summary)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        speak("That topic is too broad, can you be more specific?")
        return None
    except Exception as e:
        print("Wikipedia error:", e)
        logging.error(f"Wikipedia error: {e}")
        speak("I couldn't get the summary from Wikipedia.")
        return None

def get_weather(city):
    """Get live weather from OpenWeather API."""
    speak(f"Checking weather in {city}...")
    logging.info(f"Weather query: {city}")
    if not OPENWEATHER_API_KEY:
        speak("Weather API key is missing.")
        return None

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url).json()

        if "main" in response:
            temp = response["main"]["temp"]
            desc = response["weather"][0]["description"]
            humidity = response["main"]["humidity"]
            wind = response["wind"]["speed"]

            weather_info = f"The weather in {city} is {desc}, temperature is {temp}°C, humidity is {humidity}%, and wind speed is {wind} m/s."
            speak(weather_info)
            return weather_info
        else:
            speak("City not found or API error.")
            return None
    except Exception as e:
        print("Weather API error:", e)
        logging.error(f"Weather API error: {e}")
        speak("I couldn't retrieve weather information.")
        return None