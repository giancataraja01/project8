import time
import os

def follow(file_path, sleep_sec=1.0):
    """Display the content of the file and continue printing new entries."""
    try:
        with open(file_path, 'r') as file:
            # Read and display existing content of the file
            print("[CONTENT OF FILE]")
            file.seek(0)  # Go to the beginning of the file
            content = file.read()
            if content:
                print(content)  # Print existing content
            else:
                print("[INFO] The file is currently empty.")
                
            print("\n[START MONITORING NEW ENTRIES]")
            file.seek(0, os.SEEK_END)  # Move the pointer to the end for new entries
            
            while True:
                line = file.readline()
                if line:
                    print(line.rstrip())  # Display new line
                else:
                    time.sleep(sleep_sec)  # Wait for new content
    except FileNotFoundError:
        print(f"[ERROR] File '{file_path}' not found.")
    except KeyboardInterrupt:
        print("\n[INFO] Monitoring stopped by user.")

def main():
    log_file = "detection_logs.txt"
    print(f"Monitoring '{log_file}'... (Press Ctrl+C to stop)")
    follow(log_file)

if __name__ == "__main__":
    main()
