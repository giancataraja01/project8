import jetson.inference
import jetson.utils

# Create a text file for logging detections
log_file = open("detection_logs.txt", "w")

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = jetson.utils.gstCamera(1280, 720, "/dev/video0")
display = jetson.utils.glDisplay()

person_detected = False  # Flag to track if a person has already been logged

while display.IsOpen() and not person_detected:
    img, width, height = camera.CaptureRGBA()
    detections = net.Detect(img, width, height)

    # Check for a person in detections
    for detection in detections:
        if net.GetClassDesc(detection.ClassID).lower() == "person":
            log_file.write("true")
            log_file.flush()  # Ensure the log is written immediately
            person_detected = True  # Set the flag to stop further logging
            break

    display.RenderOnce(img, width, height)
    display.SetTitle("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

# Ensure the log file is closed when the program ends
log_file.close()
