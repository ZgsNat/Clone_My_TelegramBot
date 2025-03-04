import asyncio
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from database.google_sheets_v2 import get_user_sheet_for_current_year, format_month_worksheet, get_google_client, create_or_get_worksheet
import gspread
import calendar

async def fix_format_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Áp dụng định dạng cho các sheet theo tháng được chỉ định."""
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or f"user_{user_id}"
    
    args = context.args
    if not args:
        # Nếu không có tháng nào được chỉ định, áp dụng cho tất cả các tháng
        month_nums = list(range(1, 13))
    else:
        try:
            month_nums = [int(arg) for arg in args[0].split(',')]  
            for month_num in month_nums:
                if month_num < 1 or month_num > 12:
                    raise ValueError
        except ValueError:
            await update.message.reply_text("⚠ Vui lòng nhập số tháng hợp lệ từ 1 đến 12. Ví dụ: `/fix_format 1,3,4,5`")
            return

    months = [calendar.month_name[month_num] for month_num in month_nums]  

    sheet_id = await get_user_sheet_for_current_year(user_id, username, update)
    if not sheet_id:
        await update.message.reply_text("❌ Bạn chưa có Google Sheet.")
        return

    try:
        client = await get_google_client()
        sheet = await client.open_by_key(sheet_id)
        await update.message.reply_text("🔄 Đang áp dụng định dạng cho các sheet... \n Vui lòng chờ cho tới khi hoàn tất....")
        
        # Chia thành batch (4 tháng mỗi batch)
        batch_size = 4
        month_batches = [months[i:i + batch_size] for i in range(0, len(months), batch_size)]
        
        for batch in month_batches:
            tasks = []
            for month in batch:
                try:
                    worksheet = await create_or_get_worksheet(sheet_id, month)
                    tasks.append(format_month_worksheet(worksheet, sheet_id))
                except gspread.WorksheetNotFound:
                    await update.message.reply_text(f"❌ Không tìm thấy sheet `{month}`. Hãy kiểm tra lại số tháng.")
            
            # Chạy batch 4 sheets cùng lúc
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Kiểm tra lỗi trong batch
            for result in results:
                if isinstance(result, Exception):
                    await update.message.reply_text(f"❌ Đã xảy ra lỗi khi xử lý sheet: {result}")
            
            # Chờ 10s giữa các batch để tránh quota (giảm thời gian chờ)
            # await asyncio.sleep(10)
        
        await update.message.reply_text("✅ Đã hoàn tất áp dụng định dạng cho các sheet!")
    
    except Exception as e:
        await update.message.reply_text(f"❌ Đã xảy ra lỗi: {e}")

def get_handlers():
    return CommandHandler("fix_format", fix_format_command)