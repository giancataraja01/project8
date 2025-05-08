import time
import os

def follow(file_path, sleep_sec=1.0):
    """Yield new lines added to the file in real-time."""
    try:
        with open(file_path, 'r') as file:
            # Move to the end of file
            file.seek(0, os.SEEK_END)
            while True:
                line = file.readline()
                if not line:
                    time.sleep(sleep_sec)
                    continue
                yield line.rstrip('\n')
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")

def main():
    log_file = "detection_logs.txt"
    print(f"Monitoring '{log_file}' for new entries...\n")
    for line in follow(log_file):
        print(f"[NEW] {line}")

if __name__ == "__main__":
    main()
