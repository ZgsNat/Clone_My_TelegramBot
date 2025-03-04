import importlib
import os
from telegram.ext import Application, BaseHandler
from utils.logger import logger  # Đảm bảo bạn đã có logger đúng cách

def load_handlers(app: Application, handler_paths: list):
    for path in handler_paths:
        base_path = os.path.join(os.path.dirname(__file__), "..", path)
        
        # Đệ quy qua các thư mục con
        for root, dirs, files in os.walk(base_path):
            for file_name in files:
                if file_name.endswith(".py") and not file_name.startswith("__"):
                    # Xác định module path từ file
                    module_path = f"{path}.{os.path.relpath(os.path.join(root, file_name), base_path).replace(os.path.sep, '.')[:-3]}"
                    try:
                        module = importlib.import_module(module_path)

                        if hasattr(module, "get_handlers"):
                            handlers = module.get_handlers()
                            if isinstance(handlers, BaseHandler):  # Một handler duy nhất
                                app.add_handler(handlers)
                            elif isinstance(handlers, list):  # Danh sách handlers
                                for handler in handlers:
                                    if isinstance(handler, BaseHandler):
                                        app.add_handler(handler)
                            else:
                                logger.error(f"{module_path}.get_handlers() must return a handler or a list of handlers.")
                    except Exception as e:
                        logger.error(f"Error loading handlers from {module_path}: {e}")
