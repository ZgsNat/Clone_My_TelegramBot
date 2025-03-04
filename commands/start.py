from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, ContextTypes
from database.google_sheets_v2 import get_user_sheet_for_current_year  # Sử dụng hàm mới
from datetime import datetime

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bắt đầu cuộc trò chuyện với bot"""
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or f"user_{user_id}"
    current_year = datetime.now().year

    # Lấy hoặc tạo Google Sheet năm hiện tại
    sheet_id = await get_user_sheet_for_current_year(user_id, username, update)

    greeting = f"Chào mừng bạn tới chat quản lý thu chi {current_year}! 📊"
    
    sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}"
    keyboard = [[InlineKeyboardButton("📊 MỞ GOOGLE SHEET", url=sheet_url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"👋 Hello {username}! {greeting}\n\nQuản lý thu chi của bạn cho {current_year} ở đây:",
        reply_markup=reply_markup
    )

# Hàm trả về handler để tự động load
def get_handlers():
    return CommandHandler("start", start_command)
