from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class LogFileHandler(FileSystemEventHandler):
    def __init__(self, file_path):
        self.file_path = file_path
        self.last_position = 0

    def on_modified(self, event):
        if event.src_path.endswith(self.file_path):
            with open(self.file_path, 'r') as file:
                file.seek(self.last_position)
                new_content = file.read()
                if new_content:
                    print(new_content, end='')  # print new lines without extra newline
                self.last_position = file.tell()

def monitor_log_file(file_path):
    print(f"Monitoring '{file_path}' for real-time updates... (Press Ctrl+C to stop)")
    event_handler = LogFileHandler(file_path)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopped monitoring.")
    observer.join()

if __name__ == "__main__":
    log_file = "detection_logs.txt"
    monitor_log_file(log_file)
