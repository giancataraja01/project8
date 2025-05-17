import Jetson.GPIO as GPIO
import time

# GPIO and frequency setup
TWEETER_PIN = 7          # Pin 7 (BOARD numbering)
ULTRASONIC_FREQ = 25000  # 25 kHz
DUTY_CYCLE = 50          # 50% for square wave

# File to monitor
STATUS_FILE = "detection_logs.txt"

GPIO.setmode(GPIO.BOARD)
GPIO.setup(TWEETER_PIN, GPIO.OUT)

# Initialize PWM
pwm = GPIO.PWM(TWEETER_PIN, ULTRASONIC_FREQ)
tweeter_is_on = False

# Function to read detection status
def read_status(filename=STATUS_FILE):
    try:
        with open(filename, "r") as file:
            content = file.read().strip().lower()
            return content == "true"
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return False

print("Monitoring detection_logs.txt... Press Ctrl+C to stop.")

try:
    while True:
        status = read_status()

        if status and not tweeter_is_on:
            pwm.start(DUTY_CYCLE)
            tweeter_is_on = True
            print("Tweeter ON (25 kHz tone)")
        elif not status and tweeter_is_on:
            pwm.stop()
            tweeter_is_on = False
            print("Tweeter OFF")

        time.sleep(1)  # Check every second

except KeyboardInterrupt:
    print("Stopping...")

finally:
    pwm.stop()
    GPIO.cleanup()
    print("GPIO cleaned up. Tweeter OFF.")