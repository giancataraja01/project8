import Jetson.GPIO as GPIO
import time

# GPIO setup
TWEETER_PIN = 33  # Physical pin 33 (GPIO13)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TWEETER_PIN, GPIO.OUT)

# Turn tweeter on for 60 seconds
GPIO.output(TWEETER_PIN, GPIO.HIGH)
print("Tweeter ON")
time.sleep(60)
GPIO.output(TWEETER_PIN, GPIO.LOW)
print("Tweeter OFF")

# Cleanup GPIO
GPIO.cleanup()
