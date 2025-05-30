import cv2
import numpy as np

# Paths to the model files (download and update paths here)
MODEL_PATH = 'ssd_mobilenet_v2_coco_2018_03_29.pb'
CONFIG_PATH = 'ssd_mobilenet_v2_coco_2018_03_29.pbtxt'

# Load class names from COCO dataset
classNames = { 1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane', 6: 'bus',
               7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light', 11: 'fire hydrant',
               13: 'stop sign', 14: 'parking meter', 15: 'bench', 16: 'bird', 17: 'cat',
               18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear',
               24: 'zebra', 25: 'giraffe', 27: 'backpack', 28: 'umbrella', 31: 'handbag',
               32: 'tie', 33: 'suitcase', 34: 'frisbee', 35: 'skis', 36: 'snowboard',
               37: 'sports ball', 38: 'kite', 39: 'baseball bat', 40: 'baseball glove',
               41: 'skateboard', 42: 'surfboard', 43: 'tennis racket', 44: 'bottle',
               46: 'wine glass', 47: 'cup', 48: 'fork', 49: 'knife', 50: 'spoon',
               51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange',
               56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut',
               61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed',
               67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse',
               75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave',
               79: 'oven', 80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book',
               85: 'clock', 86: 'vase', 87: 'scissors', 88: 'teddy bear',
               89: 'hair drier', 90: 'toothbrush' }

# Load the network
net = cv2.dnn.readNetFromTensorflow(MODEL_PATH, CONFIG_PATH)

# Use GPU on Jetson Nano if available (CUDA backend)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

# Open webcam/video
cap = cv2.VideoCapture(0)  # Change to video file if needed

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Prepare input blob for the network
    blob = cv2.dnn.blobFromImage(frame, size=(300, 300), swapRB=True, crop=False)
    net.setInput(blob)

    # Run forward pass to get detections
    detections = net.forward()

    h, w = frame.shape[:2]

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        class_id = int(detections[0, 0, i, 1])

        # Filter only dogs with confidence > 0.5
        if confidence > 0.5 and class_id == 18:  # 18 is the COCO class ID for dog
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x1, y1, x2, y2) = box.astype('int')

            # Draw bounding box and label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f'Dog: {confidence:.2f}'
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow('Dog Detection - MobileNetV2 SSD', frame)

    if cv2.waitKey(1) == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
