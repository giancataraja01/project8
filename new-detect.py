import os
import sys
import argparse
import glob
import time

import cv2
import numpy as np
import torch
from torchvision.ops import nms

# Define your label names manually
labels = ['dog_with_collar', 'dog_without_collar']  # Replace as needed

# CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('--model', required=True, help='Path to PyTorch YOLO model')
parser.add_argument('--source', required=True, help='Image file, folder, video, or usb index (e.g., usb0)')
parser.add_argument('--thresh', default=0.5, type=float, help='Confidence threshold')
parser.add_argument('--resolution', default=None, help='Output resolution WxH (e.g., 640x480)')
parser.add_argument('--record', action='store_true', help='Record video output to demo1.avi')
args = parser.parse_args()

# Load model
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = torch.load(args.model, map_location=device)
model.eval().to(device)

# Parse input
img_source = args.source
source_type = ''
img_exts = ['.jpg','.jpeg','.png','.bmp']
vid_exts = ['.avi','.mp4','.mov','.mkv']
if os.path.isdir(img_source):
    source_type = 'folder'
elif os.path.isfile(img_source):
    _, ext = os.path.splitext(img_source.lower())
    source_type = 'video' if ext in vid_exts else 'image'
elif 'usb' in img_source:
    source_type = 'usb'
    usb_idx = int(img_source[3:])
else:
    print('Invalid source.')
    sys.exit(1)

# Resolution
resize = False
if args.resolution:
    resW, resH = map(int, args.resolution.lower().split('x'))
    resize = True

# Record
record = args.record
if record and source_type not in ['video', 'usb']:
    print('Recording only valid for video or usb sources.')
    sys.exit(1)
if record and not resize:
    print('Specify resolution when recording.')
    sys.exit(1)
recorder = None
if record:
    recorder = cv2.VideoWriter('demo1.avi', cv2.VideoWriter_fourcc(*'MJPG'), 30, (resW, resH))

# Image loader
if source_type == 'image':
    img_list = [img_source]
elif source_type == 'folder':
    img_list = [f for f in glob.glob(img_source + '/*') if os.path.splitext(f)[1].lower() in img_exts]
elif source_type in ['video', 'usb']:
    cap = cv2.VideoCapture(img_source if source_type == 'video' else usb_idx)
    if resize:
        cap.set(3, resW)
        cap.set(4, resH)

# Drawing colors
colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,255,255)]

# Inference loop
img_count, fps_list = 0, []
while True:
    t_start = time.perf_counter()

    if source_type in ['image', 'folder']:
        if img_count >= len(img_list):
            print('All images processed.')
            break
        frame = cv2.imread(img_list[img_count])
        img_count += 1
    else:
        ret, frame = cap.read()
        if not ret:
            print('Video/camera stream ended.')
            break

    if resize:
        frame = cv2.resize(frame, (resW, resH))

    # Preprocess
    input_size = 640
    img = cv2.resize(frame, (input_size, input_size))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_tensor = torch.from_numpy(img_rgb).float().permute(2,0,1).unsqueeze(0) / 255.0
    img_tensor = img_tensor.to(device)

    with torch.no_grad():
        output = model(img_tensor)[0]

    # Postprocess
    boxes = output[..., :4]
    scores = output[..., 4]
    class_probs = output[..., 5:]
    class_ids = torch.argmax(class_probs, dim=1)
    confs = scores * class_probs[range(len(class_ids)), class_ids]
    boxes_xyxy = torch.zeros_like(boxes)
    boxes_xyxy[:, 0] = boxes[:, 0] - boxes[:, 2] / 2
    boxes_xyxy[:, 1] = boxes[:, 1] - boxes[:, 3] / 2
    boxes_xyxy[:, 2] = boxes[:, 0] + boxes[:, 2] / 2
    boxes_xyxy[:, 3] = boxes[:, 1] + boxes[:, 3] / 2

    keep = nms(boxes_xyxy, confs, iou_threshold=0.4)
    boxes_xyxy, confs, class_ids = boxes_xyxy[keep], confs[keep], class_ids[keep]

    # Draw
    count = 0
    for i in range(len(boxes_xyxy)):
        if confs[i] < args.thresh: continue
        x1, y1, x2, y2 = boxes_xyxy[i].int().cpu().numpy()
        classid = class_ids[i].item()
        color = colors[classid % len(colors)]
        label = f"{labels[classid]}: {int(confs[i]*100)}%"
        cv2.rectangle(frame, (x1,y1), (x2,y2), color, 2)
        cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        count += 1

    # Show results
    cv2.putText(frame, f'Detections: {count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
    if source_type in ['video', 'usb']:
        fps = 1 / (time.perf_counter() - t_start)
        fps_list.append(fps)
        cv2.putText(frame, f'FPS: {fps:.2f}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
    cv2.imshow('YOLO Detection', frame)
    if record: recorder.write(frame)

    key = cv2.waitKey(0 if source_type in ['image','folder'] else 5)
    if key in [ord('q'), ord('Q')]: break
    elif key in [ord('s'), ord('S')]: cv2.waitKey()
    elif key in [ord('p'), ord('P')]: cv2.imwrite('capture.png', frame)

# Cleanup
if source_type in ['video','usb']: cap.release()
if record: recorder.release()
cv2.destroyAllWindows()
if fps_list:
    print(f'Average FPS: {sum(fps_list)/len(fps_list):.2f}')
