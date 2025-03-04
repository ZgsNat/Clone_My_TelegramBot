import config
import signal
import sys
from telegram.ext import Application
from utils.logger import setup_logger
from utils.handler_loader import load_handlers
from handlers.error_handler import error_handler_instance
from backgroundJob.background_jobs import scheduler, start_scheduler

logger = setup_logger(__name__)

def main():
    app = Application.builder().token(config.TOKEN).build()

    # Load handlers từ commands và handlers
    handler_paths = ["commands", "handlers"]
    load_handlers(app, handler_paths)

    # Thêm error handler
    app.add_error_handler(error_handler_instance)

    # Khởi động background scheduler
    start_scheduler()

    logger.info(f"🚀 Bot {config.BOT_USERNAME} đang chạy!")
    
    # Chạy bot Telegram
    app.run_polling(poll_interval=3)

# Xử lý tắt bot gọn gàng
def shutdown(signum, frame):
    logger.info("🛑 Đang tắt bot và scheduler...")
    scheduler.shutdown(wait=False)  # Tắt scheduler
    sys.exit(0)  # Thoát chương trình

if __name__ == "__main__":
    # Đăng ký tín hiệu để tắt bot gọn gàng
    signal.signal(signal.SIGINT, shutdown)  # Ctrl+C
    signal.signal(signal.SIGTERM, shutdown)  # Terminate

    main()
