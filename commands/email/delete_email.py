from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from database.google_sheets_v2 import get_user_sheet_for_current_year, delete_email_permission

async def delete_email_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xoá quyền chỉnh sửa Google Sheet của một email."""
    if not context.args:
        await update.message.reply_text("❌ Vui lòng nhập email: /delete_email <email>")
        return

    user_email = context.args[0]
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or f"user_{user_id}"
    
    # Lấy Google Sheet ID của năm hiện tại
    sheet_id = await get_user_sheet_for_current_year(user_id, username)

    if not sheet_id:
        await update.message.reply_text("❌ Bạn chưa có Google Sheet để xóa quyền.")
        return

    # Xóa quyền và phản hồi kết quả
    if await delete_email_permission(sheet_id, user_email):
        await update.message.reply_text(f"✅ Đã xoá quyền của {user_email}.")
    else:
        await update.message.reply_text(f"❌ Không tìm thấy email {user_email} hoặc không có quyền.")

def get_handlers():
    return CommandHandler("delete_email", delete_email_command)
