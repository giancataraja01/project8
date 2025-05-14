import Jetson.GPIO as GPIO
import time

# GPIO setup
TWEETER_PIN = 33  # Example: Pin 33 = GPIO13
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TWEETER_PIN, GPIO.OUT)

# Turn tweeter on (emit sound)
def tweeter_on(duration=2):
    print("Tweeter ON (ultrasonic sound)")
    GPIO.output(TWEETER_PIN, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(TWEETER_PIN, GPIO.LOW)
    print("Tweeter OFF")

# Simulated detection result
detected_objects = ["dog", "person"]

if "dog" in detected_objects:
    tweeter_on()

GPIO.cleanup()
