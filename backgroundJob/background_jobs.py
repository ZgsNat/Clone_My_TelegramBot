from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta
import asyncio
from backgroundJob.function.update_spending_limits import update_spending_limits
from backgroundJob.function.alert_user import alert_user  # Import the alert_user function
import logging

logger = logging.getLogger(__name__)

# Tạo scheduler
scheduler = BackgroundScheduler()

# Hàm chạy job update hạn mức chi tiêu
def run_update_spending_limits():
    """Chạy update_spending_limits trong event loop riêng"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(update_spending_limits())
    loop.close()

# Hàm chạy job alert_user
def run_alert_user():
    """Chạy alert_user trong event loop riêng"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(alert_user())
    loop.close()

# Lên lịch chạy vào 00:05 ngày 1 mỗi tháng
scheduler.add_job(run_update_spending_limits, CronTrigger(day=1, hour=0, minute=5))

# Lên lịch gửi thông báo /thu /chi vào 1 PM và 9:45 PM mỗi ngày
scheduler.add_job(run_alert_user, CronTrigger(hour=13, minute=30))
scheduler.add_job(run_alert_user, CronTrigger(hour=21, minute=30))

# # TEST: Chạy sau 5 giây kể từ khi khởi động
# run_time = datetime.now() + timedelta(seconds=5)
# scheduler.add_job(run_update_spending_limits, DateTrigger(run_date=run_time))

def start_scheduler():
    """Bắt đầu scheduler nếu chưa chạy"""
    if not scheduler.running:
        scheduler.start()
        print("✅ Background scheduler đã khởi động!")
