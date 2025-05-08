import time

def tail_file(file_path):
    """
    Continuously monitors a file for new content and prints it in real-time.
    """
    try:
        with open(file_path, "r") as file:
            # Move to the end of the file
            file.seek(0, 2)
            print(f"Monitoring '{file_path}' for updates...")
            
            while True:
                # Read new lines if available
                line = file.readline()
                if line:
                    print(line.strip())  # Print new content
                else:
                    time.sleep(0.5)  # Wait briefly before checking again
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except KeyboardInterrupt:
        print("\nStopped monitoring the file.")

# Path to the file to monitor
file_path = "detection_logs.txt"
tail_file(file_path)
