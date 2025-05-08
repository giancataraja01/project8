#!/usr/bin/env python3

from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput

# Initialize detection network
net = detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = videoSource("csi://0")      # '/dev/video0' for V4L2
display = videoOutput("display://0") # 'my_video.mp4' for file

# Open log file once and keep it open during the detection loop
log_file = open("detection_log.txt", "w")
log_file.write("Detection log started.\n")

while display.IsStreaming():
    img = camera.Capture()

    if img is None:  # capture timeout
        continue

    detections = net.Detect(img)

    # Log each detection to the file
    for detection in detections:
        log_file.write(
            f"Detected {net.GetClassDesc(detection.ClassID)} "
            f"at ({detection.Left:.2f},{detection.Top:.2f}) - "
            f"({detection.Right:.2f},{detection.Bottom:.2f})\n"
        )

    display.Render(img)
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

# Close the log file once the display loop ends
log_file.close()
