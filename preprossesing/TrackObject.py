import cv2


def track_object(thresh_image):
    # findcontours
    cnts = cv2.findContours(thresh_image, cv2.RETR_LIST,
                            cv2.CHAIN_APPROX_SIMPLE)[0]

    # filter by area
    xcnts = []
    coordinates = []
    s1 = 20
    for cnt in cnts:
        if s1 < cv2.contourArea(cnt):
            xcnts.append(cnt)

            # calculate moments for each contour
            M = cv2.moments(cnt)

            # calculate x,y coordinate of center
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            cv2.circle(frame, (cX, cY), 15, (0, 255, 0), -1)

            coordinates.append((cX, cY))
        # printing output
    print("\nDots number: {}".format(len(xcnts)))
    print(f"coordinates: {coordinates}")
    return coordinates


# capture frames from a camera with device index=0
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Can`t open the video file!\n");
    exit()


# loop runs if capturing has been initialized
while cap.isOpened():

    # reads frame from a camera
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)
    thresh = cv2.threshold(blurred, 230, 255, cv2.THRESH_BINARY)[1]
    track_object(thresh)

    # Display the frame
    cv2.imshow('Camera', frame)

    # Wait for 25ms
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release the camera from video capture
cap.release()

# De-allocate any associated memory usage
cv2.destroyAllWindows()