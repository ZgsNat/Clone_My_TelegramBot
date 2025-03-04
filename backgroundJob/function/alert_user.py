import json
import random
import asyncio
from backgroundJob.function.telegram_utils import send_telegram_message  # Import the function from telegram_utils

async def get_user_ids():
    """Lấy danh sách user_id từ user_sheet.json"""
    with open('user_sheets.json', 'r') as file:
        user_sheets = json.load(file)
    return list(user_sheets.keys())

async def alert_user():
    """Gửi thông báo /thu /chi cho người dùng với nội dung linh hoạt"""
    user_ids = await get_user_ids()  # Lấy danh sách user_id từ user_sheet.json

    # Các mẫu tin nhắn khác nhau
    messages = [
        "📢 Đừng quên ghi lại thu nhập và chi tiêu hôm nay nhé! Quản lý tài chính tốt giúp bạn chủ động hơn. 💰",
        "👋 Hôm nay bạn đã ghi lại chi tiêu chưa? Ghi chép mỗi ngày giúp bạn kiểm soát tài chính tốt hơn! ✍️",
        "💡 Một thói quen nhỏ, lợi ích lớn! Hãy cập nhật thu/chi hôm nay để duy trì kiểm soát tài chính nhé! 📊",
        "🔔 Nhắc nhẹ! Đừng quên ghi chép thu nhập và chi tiêu nhé. Mọi đồng tiền đều quan trọng! 💸",
        "🌟 Chăm chỉ theo dõi thu chi mỗi ngày sẽ giúp bạn đạt mục tiêu tài chính nhanh hơn! Bạn đã ghi chép chưa nào? 😉",
    ]

    for user_id in user_ids:
        message = random.choice(messages)  # Chọn ngẫu nhiên một tin nhắn
        await send_telegram_message(user_id, message)
