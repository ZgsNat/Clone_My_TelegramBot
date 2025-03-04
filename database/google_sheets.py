import gspread
import gspread_asyncio
from google.oauth2.service_account import Credentials
import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from googleapiclient.discovery import build

# Kết nối với Google Sheets API
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file"
]
CREDS = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(CREDS)
DB_FILE = "user_sheets.json"

def get_drive_service():
    """Kết nối với Google Drive API."""
    creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)


def load_user_sheets():
    """Tải danh sách user_id ↔ sheet_id từ file JSON"""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as file:
            return json.load(file)
    return {}

def save_user_sheets(data):
    """Lưu danh sách user_id ↔ sheet_id vào file JSON"""
    directory = os.path.dirname(DB_FILE)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)  # Đảm bảo thư mục tồn tại
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=4)

def get_google_client():
    """Kết nối với Google Sheets API"""
    creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    return gspread.authorize(creds)

def create_user_sheet(user_id, username="User"):
    """Tạo Google Sheet mới nếu chưa có"""
    user_sheets = load_user_sheets()

    if str(user_id) in user_sheets:
        return user_sheets[str(user_id)]  # Trả về Sheet ID nếu đã tồn tại

    client = get_google_client()
    sheet = client.create(f"{username}_Expenses")  # Tạo Google Sheet mới
    sheet.share(None, perm_type='anyone', role='reader')  # Cho phép mọi người xem

    user_sheets[str(user_id)] = sheet.id  # Lưu user_id ↔ sheet_id
    save_user_sheets(user_sheets)

    return sheet.id  # Trả về Sheet ID mới tạo

def get_user_sheet(user_id):
    """Lấy Google Sheet ID của user"""
    user_sheets = load_user_sheets()
    return user_sheets.get(str(user_id), None)

def get_worksheet(user_id):
    """Lấy worksheet của user"""
    sheet_id = get_user_sheet(user_id)
    if not sheet_id:
        return None  # User chưa có Google Sheet

    client = get_google_client()
    sheet = client.open_by_key(sheet_id)

    # Kiểm tra xem có worksheet "Categories" chưa, nếu chưa thì tạo mới
    try:
        return sheet.worksheet("Categories")
    except gspread.exceptions.WorksheetNotFound:
        return sheet.add_worksheet(title="Categories", rows=100, cols=2)

def list_permissions(sheet_id):
    """Liệt kê các email có quyền chỉnh sửa Google Sheet."""
    client = get_google_client()
    sheet = client.open_by_key(sheet_id)
    permissions = sheet.list_permissions()
    return [perm['emailAddress'] for perm in permissions if 'emailAddress' in perm]

def delete_email_permission(sheet_id, user_email):
    """Xóa quyền chỉnh sửa của email khỏi Google Sheet."""
    service = get_drive_service()
    
    try:
        permissions = service.permissions().list(
            fileId=sheet_id, 
            fields="permissions(id, emailAddress)"
        ).execute()

        for perm in permissions.get('permissions', []):
            if perm.get('emailAddress') == user_email:
                service.permissions().delete(
                    fileId=sheet_id, 
                    permissionId=perm['id']
                ).execute()
                return True
    except Exception as e:
        print(f"Error deleting permission: {e}")
    
    return False

async def send_google_sheet(update: Update, context: CallbackContext, sheet_id: str, user_email: str):
    """Send Google Sheet link to the user"""
    sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}"

    # Mở Google Sheet và chia sẻ quyền chỉnh sửa
    client = get_google_client()
    sheet = client.open_by_key(sheet_id)
    sheet.share(user_email, perm_type='user', role='writer')  # Chia sẻ quyền chỉnh sửa

    # Tạo nút "GOOGLE SHEET"
    keyboard = [[InlineKeyboardButton("📊 GOOGLE SHEET", url=sheet_url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Gửi tin nhắn với nút bấm
    await update.message.reply_text(f"Email của bạn đã được thêm! \n",f"📝 Click nút dưới đây để mở Google Sheet của bạn:", reply_markup=reply_markup)