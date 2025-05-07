import smtplib
from email.mime.text import MIMEText
from text_to_speech_module import speak
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

# Email configuration from .env
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Setup logging
logging.basicConfig(filename="aurora.log", level=logging.INFO)

def send_email(recipient, subject, body):
    """Send an email using SMTP."""
    if not all([SMTP_SERVER, SMTP_PORT, EMAIL_ADDRESS, EMAIL_PASSWORD]):
        speak("Email configuration is incomplete. Please set up SMTP details.")
        logging.error("Email configuration incomplete")
        return

    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = recipient

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipient, msg.as_string())

        speak(f"Email sent to {recipient}.")
        logging.info(f"Email sent to {recipient}: {subject}")
    except Exception as e:
        speak("Sorry, I couldn't send the email.")
        print("Email error:", e)
        logging.error(f"Email error: {e}")