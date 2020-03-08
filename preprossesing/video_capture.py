import cv2

def track_object(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)
    thresh = cv2.threshold(blurred, 230, 255, cv2.THRESH_BINARY)[1]
    # th, threshed = cv2.threshold(gray, 250, 255,
    #                              cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # findcontours
    cnts = cv2.findContours(thresh, cv2.RETR_LIST,
                            cv2.CHAIN_APPROX_SIMPLE)[0]

    # filter by area
    xcnts = []
    coordinates = []
    for cnt in cnts:
        xcnts.append(cnt)

        # calculate moments for each contour
        M = cv2.moments(cnt)

        # calculate x,y coordinate of center
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        coordinates.append((cX, cY))
        # printing output
    print("\nDots number: {}".format(len(xcnts)))
    print(f"coordinates: {coordinates}")
    return coordinates

# capture frames from a camera with device index=0
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Can`t open the video file!\n");
    exit()
# loop runs if capturing has been initialized
while True:

    # reads frame from a camera
    ret, frame = cap.read()
    track_object(frame)
    # Display the frame
    cv2.imshow('Camera', frame)

    # Wait for 25ms
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release the camera from video capture
cap.release()

# De-allocate any associated memory usage
cv2.destroyAllWindows()
