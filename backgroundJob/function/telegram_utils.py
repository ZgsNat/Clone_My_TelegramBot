from telegram import Bot
from config import TOKEN  # Import TELEGRAM_BOT_TOKEN từ config.py

bot = Bot(token=TOKEN)

async def send_telegram_message(user_id, message):
    """Gửi tin nhắn Telegram cho người dùng"""
    try:
        await bot.send_message(chat_id=user_id, text=message, parse_mode="Markdown")
    except Exception as e:
        print(f"⚠️ Không thể gửi tin nhắn cho {user_id}: {e}")