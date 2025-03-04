import gspread
import calendar
import asyncio
from datetime import datetime
from database.google_sheets_v2 import get_google_client, load_user_sheets, parse_money_input
from backgroundJob.function.telegram_utils import send_telegram_message  # Import the function from telegram_utils

async def update_spending_limits():
    """Cập nhật hạn mức chi tiêu cho tất cả người dùng nếu bị vượt quá."""
    user_sheets = await load_user_sheets()
    current_year = str(datetime.now().year)
    current_month = datetime.now().month
    prev_year, prev_month = (current_year, current_month - 1) if current_month > 1 else (str(int(current_year) - 1), 12)

    for user_id, sheets in user_sheets.items():
        sheet_id = sheets.get(current_year)
        prev_sheet_id = sheets.get(prev_year)
        
        if not sheet_id or not prev_sheet_id:
            continue  # Bỏ qua nếu không tìm thấy Google Sheet

        try:
            client = await get_google_client()
            sheet = await client.open_by_key(sheet_id)
            prev_sheet = await client.open_by_key(prev_sheet_id)

            # Lấy worksheet tháng trước và tháng hiện tại
            prev_ws = await prev_sheet.worksheet(calendar.month_name[prev_month])
            curr_ws = await sheet.worksheet(calendar.month_name[current_month])

            # Lấy dữ liệu hạn mức của tháng trước
            prev_data = await prev_ws.get("A1:Z") or []
            prev_headers = prev_data[0] if len(prev_data) > 0 else []
            prev_sub_headers = prev_data[2] if len(prev_data) > 2 else []
            prev_data_rows = prev_data[3:] if len(prev_data) > 3 else []

            # Xác định vị trí các cột quan trọng
            try:
                limit_index = prev_headers.index("Hạn mức chi tiêu")
                sub_headers_limit = prev_sub_headers[limit_index:]
                col_muc = limit_index + sub_headers_limit.index("Mục")
                col_da_chi = limit_index + sub_headers_limit.index("Đã chi")
                col_con_lai = limit_index + sub_headers_limit.index("Còn lại")
            except ValueError:
                print(f"❌ Sheet {calendar.month_name[prev_month]} thiếu bảng 'Hạn mức chi tiêu'!")
                continue

            # Duyệt qua các danh mục chi tiêu để kiểm tra hạn mức
            messages = []
            for row in prev_data_rows:
                if len(row) > col_muc and row[col_muc]:
                    category = row[col_muc].strip().lower()

                    # Chuyển đổi số tiền từ Google Sheets (nếu bị rỗng, mặc định là 0)
                    spent = parse_money_input(row[col_da_chi]) if len(row) > col_da_chi and row[col_da_chi] else 0
                    remaining = parse_money_input(row[col_con_lai]) if len(row) > col_con_lai and row[col_con_lai] else 0
                    if remaining is None:
                        remaining = 0  # Đảm bảo remaining không phải None

                    if remaining < 0:  # Nếu bị âm hạn mức
                        messages.append(f"⚠️ Hạn mức '{category}' tháng trước bị vượt quá {abs(remaining):,.0f}. Sẽ trừ vào tháng này.")

                        # Cập nhật vào sheet tháng hiện tại
                        curr_data = await curr_ws.get("A1:Z") or []
                        curr_data_rows = curr_data[3:] if len(curr_data) > 3 else []

                        updated = False  # Biến để kiểm tra xem có cập nhật hay không
                        for curr_row_index, curr_row in enumerate(curr_data_rows, start=4):
                            if len(curr_row) > col_muc and curr_row[col_muc].strip().lower() == category:
                                curr_spent = parse_money_input(curr_row[col_da_chi]) if len(curr_row) > col_da_chi and curr_row[col_da_chi] else 0
                                new_spent = curr_spent + abs(remaining)
                                await curr_ws.update_cell(curr_row_index, col_da_chi + 1, new_spent)
                                
                                # Update the remaining column
                                curr_limit = parse_money_input(curr_row[col_con_lai]) if len(curr_row) > col_con_lai and curr_row[col_con_lai] else 0
                                new_remaining = curr_limit - new_spent
                                await curr_ws.update_cell(curr_row_index, col_con_lai + 1, new_remaining)
                                
                                updated = True
                                break  # Dừng vòng lặp sau khi cập nhật

                        # Nếu không tìm thấy danh mục trong tháng này → thêm mới
                        if not updated:
                            new_row = [""] * (col_con_lai + 1)
                            new_row[col_muc] = category.capitalize()  # Viết hoa tên danh mục
                            new_row[col_da_chi] = abs(remaining)
                            new_row[col_con_lai] = -abs(remaining)  # Set the remaining to negative of the overspent amount
                            await curr_ws.append_row(new_row)

                    elif remaining > 0:
                        messages.append(f"🎉 Bạn đã tiết kiệm được {remaining:,.0f} trong mục '{category}' tháng trước! Tuyệt vời!")
                else:
                    print(f"❌ Hạn mức trống hoặc không tìm thấy ở dòng {row}")

            # Gửi thông báo đến user
            if messages:
                text = "\n".join(messages)
                await send_telegram_message(user_id, text)

        except Exception as e:
            print(f"❌ Lỗi khi cập nhật hạn mức cho user {user_id}: {e}")
