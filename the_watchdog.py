import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, file_path):
        self.file_path = file_path

    def on_modified(self, event):
        if event.src_path == self.file_path:
            print(f"File '{self.file_path}' has been modified. New contents:")
            self.display_file_contents()

    def display_file_contents(self):
        try:
            with open(self.file_path, 'r') as file:
                print(file.read())
        except Exception as e:
            print(f"Error reading file: {e}")


if __name__ == "__main__":
    file_to_watch = "text-reader.py"  # Change this to the file you want to monitor

    event_handler = FileChangeHandler(file_to_watch)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)

    print(f"Watching for changes in '{file_to_watch}'...")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
