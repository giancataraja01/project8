import time

def read_file_in_real_time(file_path):
    """
    Continuously reads a file and displays new content in real-time.
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
                    print(line.strip())  # Print new content without extra whitespace
                else:
                    time.sleep(0.5)  # Wait briefly before checking again
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except KeyboardInterrupt:
        print("\nStopped monitoring the file.")

# Path to the file to monitor
file_path = "detection_logs.txt"
read_file_in_real_time(file_path)
