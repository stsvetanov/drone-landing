import cv2
import numpy as np
from utils import find_blobs, calculate_positions

capture = cv2.VideoCapture(0)

if not capture.isOpened():
    print("Can`t open the video file!\n");
    exit()

while capture.isOpened():
    # print(f'FPS: {cv2.CAP_PROP_FPS}')
    ret, frame = capture.read()
    coordinates = find_blobs(frame)
    # if len(coordinates) == 5:
    #     calculate_positions(coordinates, frame)

    cv2.imshow('Camera', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.imshow("Output", capture)
cv2.waitKey(0)
