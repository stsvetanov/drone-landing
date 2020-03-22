# Да се създаде програма, кото проверява за дефектни детайли.
# Да проверява дъжината на детайла и дали е крив.
# Допълнително условие, да проверява да детайлът е остър.
# Допълнително условие, да се синхронизира с вход от потребителия, т.е. блокираща комуникация.

import cv2
from scipy.spatial import distance as dist

scale = 0.182
cam_id = 1

def midpoint(ptA, ptB):
    return (int((ptA[0] + ptB[0]) * 0.5), int((ptA[1] + ptB[1]) * 0.5))


def track_object(thresh_image):
    # findcontours
    cnts = cv2.findContours(thresh_image, cv2.RETR_TREE,
                            cv2.CHAIN_APPROX_SIMPLE)[0]

    # filter by area
    s1 = 20
    defect = False
    for cnt in cnts:
        if s1 < cv2.contourArea(cnt):
            # cv2.drawContours(frame, [cnt], 0, (0, 255, 0), 6)

            epsilon = 0.1 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True);
            cv2.drawContours(frame, approx, -1, (0, 255, 0), 6)
            # cv2.line(frame, tuple(approx[0][0]), tuple(approx[1][0]), (0, 255, 100), 4)
            if len(approx) == 2:
                for i in range(-1, 1):
                    cv2.line(frame, tuple(approx[i - 1][0]), tuple(approx[i][0]), (0, 255, 0), 4)
                    size_pixels = dist.euclidean(tuple(approx[i - 1][0]), tuple(approx[i][0]))
                    size_mm = size_pixels * scale
                    position = midpoint(tuple(approx[i - 1][0]), tuple(approx[i][0]))
                    cv2.putText(frame, f"{round(size_mm, 1)}", position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA)
            else:
                return True

            # calculate moments for each contour
            M = cv2.moments(cnt)

            # calculate x,y coordinate of center
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            # Да се добавят останалите услувия
            cv2.circle(frame, (cX, cY), 4, (0, 255, 0), -1)

        if 32 < size_mm < 38:
            defect = True

    return defect


# capture frames from a camera with device index=0
cap = cv2.VideoCapture(cam_id)

if not cap.isOpened():
    print("Can`t open the video file!\n");
    exit()


# loop runs if capturing has been initialized
while cap.isOpened():
    # Да се сихнронизира с вход от потребителя.
    # continue_key = input("Put next detail")

    # reads frame from a camera
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)
    thresh = cv2.threshold(blurred, 160, 255, cv2.THRESH_BINARY)[1]
    defect = track_object(thresh)
    print(f"Defect detail!: {defect}")

    # Display the frame
    cv2.imshow('Camera', frame)

    # Wait for 25ms
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release the camera from video capture
cap.release()

# De-allocate any associated memory usage
cv2.destroyAllWindows()