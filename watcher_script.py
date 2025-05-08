import time
import os

def follow(file_path, sleep_sec=1.0):
    """Yield new lines appended to a file in real time."""
    try:
        with open(file_path, 'r') as file:
            # Go to the end of the file
            file.seek(0, os.SEEK_END)
            while True:
                line = file.readline()
                if line:
                    print(line.rstrip())  # Display new line without extra newline
                else:
                    time.sleep(sleep_sec)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except KeyboardInterrupt:
        print("\nStopped monitoring.")

def main():
    log_file = "detection_logs.txt"
    print(f"Monitoring '{log_file}'... (Press Ctrl+C to stop)")
    follow(log_file)

if __name__ == "__main__":
    main()
