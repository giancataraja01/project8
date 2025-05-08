import time
import os  # Needed for os.SEEK_END

def read_file_in_real_time(file_path):
    """
    Continuously reads a file and displays new content in real-time.
    """
    try:
        with open(file_path, "r") as file:
            # Move to the end of the file
            file.seek(0, os.SEEK_END)
            print("Monitoring '{}' for updates...".format(file_path))
            
            while True:
                # Read new lines if available
                line = file.readline()
                if line:
                    print(line.strip())  # Print new content without extra whitespace
                else:
                    time.sleep(0.5)  # Wait briefly before checking again
    except FileNotFoundError:
        print("Error: The file '{}' does not exist.".format(file_path))
    except KeyboardInterrupt:
        print("\nStopped monitoring the file.")

# Path to the file to monitor
file_path = "detection_logs.txt"
read_file_in_real_time(file_path)
