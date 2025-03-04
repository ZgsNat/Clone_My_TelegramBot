from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from database.google_sheets_v2 import add_expend, update_expend_limit_after_spending
from datetime import datetime

async def add_expend_command(update: Update, context: CallbackContext):
    """Thêm chi tiêu vào bảng Google Sheets."""
    user_id = update.effective_user.id
    username = update.effective_user.username
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        amount, category, description = ' '.join(context.args).split(',')
    except ValueError:
        await update.message.reply_text("❌ Vui lòng nhập đúng định dạng: /add_expend <số tiền>, <loại>, <mô tả>")
        return

    # Ghi nhận chi tiêu
    result = await add_expend(user_id, username, date, amount.strip(), category.strip(), description.strip())
    await update.message.reply_text(result)

    # ✅ Cập nhật hạn mức chi tiêu sau khi ghi nhận chi tiêu
    current_month = datetime.now().strftime("%m")
    response = await update_expend_limit_after_spending(user_id, username, current_month, category, amount)
    await update.message.reply_text(response)


def get_handlers():
    return [
        CommandHandler("chi", add_expend_command),
    ]