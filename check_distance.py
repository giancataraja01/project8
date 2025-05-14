import Jetson.GPIO as GPIO
import time

# File to monitor
FILE_PATH = 'detection_logs.txt'

# GPIO pin setup (BCM numbering)
TRIG = 23  # Adjust as per your wiring
ECHO = 24  # Adjust as per your wiring

# GPIO setup
GPIO.setmode(GPIO.BCM)
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

    # Wait for echo start
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    # Wait for echo end
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # Calculate duration
    pulse_duration = pulse_end - pulse_start

    # Calculate distance (in cm)
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance

try:
    while True:
        if read_trigger_file():
            dist = measure_distance()
            print(f"Distance: {dist} cm")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nMeasurement stopped by User")
    GPIO.cleanup()
