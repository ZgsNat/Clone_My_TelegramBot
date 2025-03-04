from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from database.google_sheets_v2 import update_expend_limit, update_expend_limit_after_spending
import datetime

async def update_expend_limit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Thay đổi hạn mức chi tiêu cho một tháng hoặc từ tháng hiện tại đến cuối năm."""
    user_id = update.effective_user.id
    username = update.effective_user.username

    if len(context.args) < 1:
        await update.message.reply_text("❌ Sai cú pháp! Dùng: `/update_expend_limit <Tháng hoặc all>,<Hạn mức>,<Mục>`")
        return

    # Ghép lại toàn bộ input để xử lý đúng cú pháp có dấu phẩy
    full_input = " ".join(context.args)
    parts = [p.strip() for p in full_input.split(",")]

    if len(parts) < 2:
        await update.message.reply_text("❌ Sai cú pháp! Dùng: `/update_expend_limit <Tháng hoặc all>,<Hạn mức>,<Mục>`")
        return

    month_input = parts[0].lower().strip()
    input_limit = parts[1].strip()
    category = (parts[2] if len(parts) > 2 else "Chung").lower().strip()

    # Xử lý tháng nhập vào
    if month_input == "0":
        await update.message.reply_text("❌ Tháng không hợp lệ! Nhập số từ 1-12 hoặc 'all'.")
        return

    result_message = await update_expend_limit(user_id, username, month_input, input_limit, category)
    await update.message.reply_text(result_message)
    response = await update_expend_limit_after_spending(user_id, username, month_input, category, "0")
    await update.message.reply_text(response)

def get_handlers():
    return CommandHandler('limit', update_expend_limit_command)
