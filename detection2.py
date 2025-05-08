import jetson.inference
import jetson.utils

# Create a text file for logging detections
log_file = open("detection_logs.txt", "w")
log_file.write("Detection Logs\n")
log_file.write("====================\n")

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = jetson.utils.gstCamera(1280, 720, "/dev/video0")
display = jetson.utils.glDisplay()

while display.IsOpen():
    img, width, height = camera.CaptureRGBA()
    detections = net.Detect(img, width, height)

    # Log each detection to the file
    for detection in detections:
        log_file.write("Class: {} | Confidence: {:.2f} | Location: ({:.1f}, {:.1f}, {:.1f}, {:.1f})\n".format(
            net.GetClassDesc(detection.ClassID),
            detection.Confidence,
            detection.Left,
            detection.Top,
            detection.Right,
            detection.Bottom
        ))

    display.RenderOnce(img, width, height)
    display.SetTitle("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

# Ensure the log file is closed when the program ends
log_file.close()
