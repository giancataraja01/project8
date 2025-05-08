import time
import os

def follow(file_path, sleep_sec=1.0):
    """Display the contents of the file and print new lines as they are appended."""
    try:
        with open(file_path, 'r') as file:
            # Read and print the existing content in the file
            print("[CONTENT OF FILE]")
            file.seek(0)  # Go to the beginning of the file
            print(file.read())  # Display current content of the file
            print("\n[START MONITORING NEW ENTRIES]")
            
            # Go to the end of the file and wait for new lines
            file.seek(0, os.SEEK_END)
            while True:
                line = file.readline()
                if line:
                    print(line.rstrip())  # Display new line
                else:
                    time.sleep(sleep_sec)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")

def main():
    log_file = "detection_logs.txt"
    print(f"Monitoring '{log_file}'... (Press Ctrl+C to stop)")
    follow(log_file)

if __name__ == "__main__":
    main()
