from telegram import Update
from telegram.ext import BaseHandler, ContextTypes
import logging

class ErrorHandler(BaseHandler):
    def __init__(self, callback):
        super().__init__(callback)

    def check_update(self, update):
        return True  # This handler will handle all updates

    async def handle_update(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            await self.callback(update, context)
        except Exception as e:
            logging.error(f"An error occurred: {e}")

    async def __call__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.handle_update(update, context)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"An error occurred: {context.error}")
    if update and update.message:
        await update.message.reply_text("An error occurred. Please try again later.")

# Create an instance of ErrorHandler
error_handler_instance = ErrorHandler(error_handler)