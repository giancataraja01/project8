#!/usr/bin/env python3
#
# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
# (License omitted here for brevity — same as original)
#

from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput

# Initialize detection network
net = detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = videoSource("csi://0")      # '/dev/video0' for V4L2
display = videoOutput("display://0") # 'my_video.mp4' for file

# Create or overwrite the log file when the camera starts
with open("detection_log.txt", "w") as log_file:
    log_file.write("Detection log started.\n")

    while display.IsStreaming():
        img = camera.Capture()

        if img is None:  # capture timeout
            continue

        detections = net.Detect(img)

        # Example logging of detections (optional)
        for detection in detections:
            log_file.write(f"Detected {net.GetClassDesc(detection.ClassID)} "
                           f"at ({detection.Left},{detection.Top}) - "
                           f"({detection.Right},{detection.Bottom})\n")

        display.Render(img)
        display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
