import requests

def translate_text(text, target_language="en"):
    """
    Translate text to the specified target language (default: English).
    target_language: ISO 639-1 code (e.g., 'en' for English, 'es' for Spanish).
    """
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "auto",
            "tl": target_language,
            "dt": "t",
            "q": text
        }
        response = requests.get(url, params=params)
        result = response.json()
        return result[0][0][0]
    except Exception as e:
        print("❌ Translation error:", e)
        return text  # fallback if translation fails