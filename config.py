import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_DEFAULT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME", "@YourBotName")
DB_PATH = os.getenv("DB_PATH", "database/expenses.db")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY","1234567890")
# # Print the loaded values for debugging
# print(f"TOKEN: {TOKEN}")
# print(f"BOT_USERNAME: {BOT_USERNAME}")
# print(f"DB_PATH: {DB_PATH}")
# print(f"OPENAI_API_KEY: {OPENAI_API_KEY}")