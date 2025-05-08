import jetson.inference
import jetson.utils

# Load the object detection model
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = jetson.utils.gstCamera(1280, 720, "/dev/video0")
display = jetson.utils.glDisplay()

while display.IsOpen():
    img, width, height = camera.CaptureRGBA()
    detections = net.Detect(img, width, height)

    # Filter detections to only include dogs
    dog_detections = []
    for detection in detections:
        if net.GetClassDesc(detection.ClassID).lower() == "dog":
            dog_detections.append(detection)

    # Render the filtered detections
    for detection in dog_detections:
        jetson.utils.cudaDrawRect(img, detection.ROI, (255, 0, 0, 255))  # Draw bounding box in red
        jetson.utils.cudaDrawText(
            img,
            f"Dog: {detection.Confidence * 100:.1f}%",
            (int(detection.Left), int(detection.Top) - 10),
            (255, 0, 0, 255),
        )

    display.RenderOnce(img, width, height)
    display.SetTitle("Dog Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
