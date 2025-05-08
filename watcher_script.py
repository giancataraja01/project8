import time
import os

def follow(file_path, sleep_sec=1.0):
    """Monitor and print new lines added to the file."""
    print(f"[DEBUG] Attempting to open '{file_path}'...")
    try:
        with open(file_path, 'r') as file:
            file.seek(0, os.SEEK_END)
            print(f"[DEBUG] Now monitoring '{file_path}'...")
            while True:
                line = file.readline()
                if line:
                    print(f"[NEW] {line.rstrip()}")
                else:
                    print("[DEBUG] No new line. Sleeping...")
                    time.sleep(sleep_sec)
    except FileNotFoundError:
        print(f"[ERROR] File '{file_path}' not found.")
    except KeyboardInterrupt:
        print("\n[INFO] Monitoring stopped by user.")

def main():
    log_file = "detection_logs.txt"
    follow(log_file)

if __name__ == "__main__":
    main()
