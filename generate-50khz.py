import time
import os

# Paths to the Jetson Nano PWM interface
PWM_CHIP = "0"        # pwmchip0
PWM_CHANNEL = "0"     # pwm0
PWM_BASE = f"/sys/class/pwm/pwmchip{PWM_CHIP}"
PWM_PATH = f"{PWM_BASE}/pwm{PWM_CHANNEL}"

FREQ_HZ = 50000  # 50 kHz
PERIOD_NS = int(1e9 / FREQ_HZ)  # Convert to nanoseconds
DUTY_NS = PERIOD_NS // 2        # 50% duty cycle

STATUS_FILE = "detection_logs.txt"

# Helper functions
def write_sysfs(path, value):
    with open(path, "w") as f:
        f.write(str(value))

def export_pwm():
    if not os.path.exists(PWM_PATH):
        write_sysfs(f"{PWM_BASE}/export", PWM_CHANNEL)
        time.sleep(0.1)

def unexport_pwm():
    if os.path.exists(PWM_PATH):
        write_sysfs(f"{PWM_BASE}/unexport", PWM_CHANNEL)

def start_pwm():
    write_sysfs(f"{PWM_PATH}/period", PERIOD_NS)
    write_sysfs(f"{PWM_PATH}/duty_cycle", DUTY_NS)
    write_sysfs(f"{PWM_PATH}/enable", 1)

def stop_pwm():
    write_sysfs(f"{PWM_PATH}/enable", 0)

def read_status(filename=STATUS_FILE):
    try:
        with open(filename, "r") as file:
            return file.read().strip().lower() == "true"
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return False

# Main program
print("Setting up PWM on Jetson Nano...")

export_pwm()
pwm_is_on = False

print("Monitoring detection_logs.txt... Press Ctrl+C to stop.")
try:
    while True:
        status = read_status()

        if status and not pwm_is_on:
            start_pwm()
            pwm_is_on = True
            print("PWM 50 kHz ON")

        elif not status and pwm_is_on:
            stop_pwm()
            pwm_is_on = False
            print("PWM 50 kHz OFF")

        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping...")

finally:
    stop_pwm()
    unexport_pwm()
    print("PWM stopped and cleaned up.")
