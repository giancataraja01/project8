import Jetson.GPIO as GPIO
import time

# Constants
PIN = 18                # GPIO pin (BCM numbering)
START_FREQ = 20000      # Start frequency in Hz
END_FREQ = 40000        # End frequency in Hz
STEP = 1000             # Frequency increment in Hz
TONE_DURATION = 2       # Duration of each tone in seconds

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)

# Setup PWM
pwm = GPIO.PWM(PIN, START_FREQ)

print("Starting ultrasonic frequency sweep...")
try:
    for freq in range(START_FREQ, END_FREQ + 1, STEP):
        print(f"Playing {freq} Hz")
        pwm.ChangeFrequency(freq)
        pwm.start(50)  # 50% duty cycle
        time.sleep(TONE_DURATION)
        pwm.stop()
        time.sleep(0.5)  # short pause between tones

except KeyboardInterrupt:
    print("Sweep interrupted by user.")

finally:
    pwm.stop()
    GPIO.cleanup()
    print("GPIO cleaned up. Done.")