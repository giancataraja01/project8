import time
import os

def read_file_in_real_time(file_path):
    try:
        with open(file_path, "r") as file:
            file.seek(0, os.SEEK_END)
            print("Monitoring '{}' for updates...".format(file_path))

            while True:
                line = file.readline()
                if line:
                    print("New line:", line.strip())
                else:
                    time.sleep(0.5)
    except FileNotFoundError:
        print("Error: The file '{}' does not exist.".format(file_path))
    except KeyboardInterrupt:
        print("\nStopped monitoring the file.")

file_path = "detection_logs.txt"
read_file_in_real_time(file_path)
