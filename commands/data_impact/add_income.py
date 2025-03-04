from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from database.google_sheets_v2 import add_income
from datetime import datetime

async def add_income_command(update: Update, context: CallbackContext):
    """Thêm thu nhập vào bảng Google Sheets."""
    user_id = update.effective_user.id
    username = update.effective_user.username
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        amount, category, description = ' '.join(context.args).split(',')
    except ValueError:
        await update.message.reply_text("❌ Vui lòng nhập đúng định dạng: /add_income <số tiền>, <loại>, <mô tả>")
        return

    result = await add_income(user_id, username, date, amount.strip(), category.strip(), description.strip())
    await update.message.reply_text(result)

def get_handlers():
    return [
        CommandHandler("thu", add_income_command),
    ]