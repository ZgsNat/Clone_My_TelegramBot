from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from database.google_sheets_v2 import add_saving
from datetime import datetime

async def add_saving_command(update: Update, context: CallbackContext):
    """Thêm tiết kiệm vào bảng Google Sheets."""
    user_id = update.effective_user.id
    username = update.effective_user.username
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        amount, category, description = ' '.join(context.args).split(',')
    except ValueError:
        await update.message.reply_text("❌ Vui lòng nhập đúng định dạng: /add_saving <số tiền>, <loại>, <mô tả>")
        return

    result = await add_saving(user_id, username, date, amount.strip(), category.strip(), description.strip())
    await update.message.reply_text(result)

def get_handlers():
    return [
        CommandHandler("save", add_saving_command),
    ]