from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    response = f"You said: {text}"
    await update.message.reply_text(response)

def get_handler():
    return MessageHandler(filters.TEXT, handle_message)