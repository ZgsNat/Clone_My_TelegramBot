from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, ContextTypes
from database.google_sheets_v2 import send_google_sheet, get_user_sheet_for_current_year  

async def apply_email_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Chia sẻ Google Sheet qua email"""
    if not context.args:
        await update.message.reply_text("❗ Hãy nhập email: /apply_email <your_email>")
        return

    user_email = context.args[0]
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or f"user_{user_id}"

    # Lấy Google Sheet ID của năm hiện tại
    sheet_id = await get_user_sheet_for_current_year(user_id, username)

    if not sheet_id:
        await update.message.reply_text("❗ Bạn chưa có Google Sheet. Hãy dùng /start trước.")
        return

    try:
        # Chia sẻ Google Sheet qua email
        await send_google_sheet(update, context, sheet_id, user_email)
    except Exception as e:
        await update.message.reply_text(f"❌ Lỗi khi chia sẻ: {e}")

def get_handlers():
    return [CommandHandler("apply_email", apply_email_command)]
