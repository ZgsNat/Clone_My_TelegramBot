from telegram.ext import BaseHandler, CallbackContext
from telegram import Update

class ErrorHandler(BaseHandler):
    def __init__(self, callback):
        super().__init__(callback)

    def check_update(self, update):
        return True  # This handler will handle all updates

    def handle_update(self, update: Update, context: CallbackContext):
        try:
            return self.callback(update, context)
        except Exception as e:
            context.bot.logger.error(f"An error occurred: {e}")

def error_handler(update: Update, context: CallbackContext):
    context.bot.logger.error(f"Update {update} caused error {context.error}")

# Usage
error_handler_instance = ErrorHandler(error_handler)
