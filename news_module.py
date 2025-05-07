import requests
from dotenv import load_dotenv
import os
from text_to_speech_module import speak
import logging

# Setup logging
logging.basicConfig(filename="aurora.log", level=logging.INFO)

# Load environment variables
load_dotenv()
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
NEWSAPI_URL = "https://newsapi.org/v2/top-headlines"

def get_news(query=None, max_articles=3):
    """Fetch news headlines or topic-specific news using NewsAPI."""
    if not NEWSAPI_KEY:
        speak("News API key is missing. Please configure it.")
        logging.error("NewsAPI key not found in .env")
        return

    params = {
        "apiKey": NEWSAPI_KEY,
        "pageSize": max_articles,
        "language": "en",
        "sortBy": "publishedAt"
    }

    if query:
        params["q"] = query
        logging.info(f"Fetching news for query: {query}")
    else:
        params["country"] = "us"
        logging.info("Fetching general US news headlines")

    try:
        response = requests.get(NEWSAPI_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if data["status"] != "ok" or not data.get("articles"):
            speak("Sorry, I couldn't fetch the news right now.")
            logging.error(f"NewsAPI error: {data.get('message', 'No articles found')}")
            return

        articles = data["articles"]
        if not articles:
            speak("No news articles found for that query.")
            logging.info(f"No articles found for query: {query}")
            return

        speak(f"Here are the latest news headlines{' about ' + query if query else ''}:")
        for i, article in enumerate(articles, 1):
            title = article.get("title", "No title")
            source = article.get("source", {}).get("name", "Unknown source")
            summary = article.get("description", "No summary available")
            speak(f"Headline {i} from {source}: {title}. Summary: {summary}")
            logging.info(f"News article {i}: {title} from {source}")

    except requests.RequestException as e:
        speak("Sorry, there was an error fetching the news.")
        logging.error(f"NewsAPI request failed: {str(e)}")