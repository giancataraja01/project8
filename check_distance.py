import Jetson.GPIO as GPIO
import time

# File to monitor
FILE_PATH = 'detection_logs.txt'

# GPIO pin setup (BOARD numbering assumed due to pin numbers 35 & 33)
TRIG = 35  # Physical pin 35
ECHO = 33  # Physical pin 33

# GPIO setup
GPIO.setmode(GPIO.BOARD)  # Use GPIO.BCM if using BCM numbering instead
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def read_trigger_file():
    try:
        with open(FILE_PATH, 'r') as file:
            content = file.read().strip().lower()
            return content == 'true'
    except FileNotFoundError:
        return False

def measure_distance():
    # Ensure trigger is low
    GPIO.output(TRIG, False)
    time.sleep(0.1)

    # Send 10us pulse to trigger
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Wait for echo start with timeout
    timeout_start = time.time()
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if time.time() - timeout_start > 1:
            print("Timeout: ECHO signal did not go high")
            return None

    # Wait for echo end with timeout
    timeout_end = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if time.time() - timeout_end > 1:
            print("Timeout: ECHO signal did not go low")
            return None

    # Calculate pulse duration and distance
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # cm
    distance = round(distance, 2)
    return distance

try:
    while True:
        if read_trigger_file():
            dist = measure_distance()
            if dist is not None:
                print(f"Distance: {dist} cm")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nMeasurement stopped by User")
    GPIO.cleanup()
