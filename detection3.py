import jetson.inference
import jetson.utils

# Load the object detection model
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = jetson.utils.gstCamera(1280, 720, "/dev/video0")
display = jetson.utils.glDisplay()

while display.IsOpen():
    img, width, height = camera.CaptureRGBA()
    detections = net.Detect(img, width, height)

    # Flag to check if a dog is detected
    dog_detected = False

    # Check for a dog in detections
    for detection in detections:
        if net.GetClassDesc(detection.ClassID).lower() == "dog":
            dog_detected = True
            break  # Break after detecting a dog to avoid redundant checks

    # Create or overwrite the log file and write the detection result
    with open("detection_logs.txt", "w") as log_file:
        if dog_detected:
            log_file.write("true\n")
        else:
            log_file.write("false\n")

    display.RenderOnce(img, width, height)
    display.SetTitle("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
