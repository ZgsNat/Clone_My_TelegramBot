from google.oauth2.service_account import Credentials
from database.google_sheets_v2 import get_worksheet

CATEGORY_SHEET_NAME = "Categories"

async def get_categories(user_id):
    """Lấy danh sách categories từ worksheet"""
    worksheet = await get_worksheet(user_id)
    if not worksheet:
        return []  # Trả về danh sách rỗng nếu không có worksheet

    # Lấy tất cả các giá trị từ cột đầu tiên
    categories = await worksheet.col_values(1)
    return categories

async def add_category(user_id, category_name):
    """Thêm category mới vào Google Sheets."""
    worksheet = await get_worksheet(user_id)
    if not worksheet:
        return "Không tìm thấy Google Sheet của bạn."

    categories = await get_categories(user_id)
    if category_name in categories:
        return "Category đã tồn tại!"

    await worksheet.append_row([category_name])
    return f"Đã thêm category: {category_name}"

async def delete_category(user_id, category_name):
    """Xóa category khỏi Google Sheets."""
    worksheet = await get_worksheet(user_id)
    if not worksheet:
        return "Không tìm thấy Google Sheet của bạn."

    data = await worksheet.get_all_values()
    for idx, row in enumerate(data, start=1):
        if row and row[0] == category_name:
            await worksheet.delete_rows(idx)
            return f"Đã xóa category: {category_name}"

    return "Category không tồn tại!"

async def update_category(user_id, old_name, new_name):
    """Cập nhật tên category."""
    worksheet = await get_worksheet(user_id)
    if not worksheet:
        return "Không tìm thấy Google Sheet của bạn."

    data = await worksheet.get_all_values()
    for idx, row in enumerate(data, start=1):
        if row and row[0] == old_name:
            await worksheet.update_cell(idx, 1, new_name)
            return f"Đã cập nhật category: {old_name} → {new_name}"

    return "Category không tồn tại!"
