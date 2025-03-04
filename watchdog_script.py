# filepath: /e:/FolderCode/Telegrambot/Telegram_Bot/watchdog_script.py
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class Watcher:
    DIRECTORY_TO_WATCH = "."

    def __init__(self):
        self.observer = Observer()
        self.bot_process = None

    def run(self):
        event_handler = Handler(self)
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        self.start_bot()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
            self.stop_bot()
            print("Observer Stopped")

        self.observer.join()

    def start_bot(self):
        self.bot_process = subprocess.Popen([".venv/Scripts/python", "main.py"])
        print("Bot started")

    def stop_bot(self):
        if self.bot_process:
            self.bot_process.terminate()
            self.bot_process.wait()
            print("Bot stopped")

    def restart_bot(self):
        self.stop_bot()
        self.start_bot()

class Handler(FileSystemEventHandler):
    def __init__(self, watcher):
        self.watcher = watcher

    def on_any_event(self, event):
        if event.is_directory:
            return None

        elif event.event_type == 'modified':
            # Ignore changes in the .venv and __pycache__ directories
            if '.venv' in event.src_path or '__pycache__' in event.src_path:
                return None

            # Restart the bot
            print(f"Received modified event - {event.src_path}")
            self.watcher.restart_bot()

if __name__ == '__main__':
    w = Watcher()
    w.run()