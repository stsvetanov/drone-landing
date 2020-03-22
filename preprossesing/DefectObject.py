# Да се създаде програма, кото проверява за дефектни детайли.
# Да проверява дъжината на детайла и дали е крив.
# Допълнително условие, да проверява да детайлът е остър.
# Допълнително условие, да се синхронизира с вход от потребителия, т.е. блокираща комуникация.

import cv2
from scipy.spatial import distance as dist

scale = 0.182
cam_id = 0
min_length = 36
max_length = 39


def midpoint(ptA, ptB):
    return (int((ptA[0] + ptB[0]) * 0.5), int((ptA[1] + ptB[1]) * 0.5))


def check_detail(thresh_image):
    # findcontours
    cnts = cv2.findContours(thresh_image, cv2.RETR_TREE,
                            cv2.CHAIN_APPROX_SIMPLE)[0]

    # filter by area
    s1 = 20
    check_pass = True
    if not cnts:
        print("No detail detected")
        return False
    print(len(cnts))
    for cnt in cnts:
        if s1 < cv2.contourArea(cnt):
            # cv2.drawContours(frame, [cnt], 0, (0, 255, 0), 6)

            epsilon = 0.1 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True);
            cv2.drawContours(frame, approx, -1, (0, 255, 0), 6)
            # cv2.line(frame, tuple(approx[0][0]), tuple(approx[1][0]), (0, 255, 100), 4)
            if len(approx) == 2:
                for i in range(-1, 1):
                    a = tuple(approx[i - 1][0])
                    b = tuple(approx[i][0])
                    cv2.line(frame, a, b, (0, 255, 0), 4)
                    size_pixels = dist.euclidean(a, b)
                    size_mm = size_pixels * scale
                    position = midpoint(a, b)
                    cv2.putText(frame, f"{round(size_mm, 1)}", position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA)
                if not min_length < size_mm < max_length:
                    check_pass = False

                # calculate moments for each contour
                M = cv2.moments(cnt)

                # calculate x,y coordinate of center
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                # Да се добавят останалите услувия
                cv2.circle(frame, (cX, cY), 4, (0, 255, 0), -1)

                cross_line = abs(dist.euclidean((cX, cY), a) + dist.euclidean((cX, cY), b) - size_pixels)
                print(cross_line)
                if cross_line > 3:
                    check_pass = False
    return check_pass


# capture frames from a camera with device index=0
cap = cv2.VideoCapture(cam_id)

if not cap.isOpened():
    print("Can`t open the video file!\n");
    exit()


# loop runs if capturing has been initialized
while cap.isOpened():
    # Да се сихнронизира с вход от потребителя.
    continue_key = input("Put next detail")

    # reads frame from a camera
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)
    thresh = cv2.threshold(blurred, 140, 255, cv2.THRESH_BINARY)[1]
    check = check_detail(thresh)
    if check:
        print("The detail is NOT defective!")
    else:
        print("The detail IS defective!")

    # Display the frame
    cv2.imshow('Camera', frame)

    # Wait for 25ms
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release the camera from video capture
cap.release()

# De-allocate any associated memory usage
cv2.destroyAllWindows()