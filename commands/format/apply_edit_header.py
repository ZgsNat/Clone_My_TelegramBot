from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from database.google_sheets_v2 import get_user_sheet_for_current_year, format_month_worksheet, get_google_client, create_or_get_worksheet, protect_range, remove_all_protected_ranges

async def apply_edit_header(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mở quyền điều chỉnh cho header của tất cả các tháng."""
    user_id = update.effective_user.id
    username = update.effective_user.username

    # Get the current year sheet
    sheet_id = await get_user_sheet_for_current_year(user_id, username, update)
    client = await get_google_client()

    # Apply formatting to each month's worksheet and protect the header
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    for month in months:
        ws = await create_or_get_worksheet(sheet_id, month)  # Pass correct parameters
        # await format_month_worksheet(ws, sheet_id)
        await remove_all_protected_ranges(ws)
        # await protect_range(ws, "A1:O3")  # Protect the header range

    await update.message.reply_text("✅ Headers have been formatted and protected for all months.")

# Add this function to your command handler
def get_handlers():
    return CommandHandler('apply_edit_header', apply_edit_header)