from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from database.google_sheets_v2 import get_user_sheet_for_current_year, list_permissions

async def list_emails_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Liệt kê các email được cấp quyền chỉnh sửa Google Sheet của năm hiện tại"""
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or f"user_{user_id}"
    
    # Lấy Google Sheet ID của năm hiện tại
    sheet_id = await get_user_sheet_for_current_year(user_id, username, update)

    if sheet_id:
        emails = await list_permissions(sheet_id)  # Lấy danh sách email bất đồng bộ
        if emails:
            email_list = "\n".join([f"{i+1}. {email}" for i, email in enumerate(emails)])
            await update.message.reply_text(f"📧 Các email được cấp quyền:\n{email_list}")
        else:
            await update.message.reply_text("📭 Không có email nào được cấp quyền.")
    else:
        await update.message.reply_text("❌ Bạn chưa có Google Sheet.")

def get_handlers():
    return CommandHandler("list_emails", list_emails_command)
