import cv2

# path = "white dot.png"
path = "../images/drone_station2.png"

# reading the image in grayscale mode

# show image
# cv2.imshow('image', gray)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
def find_coords(path):
    gray = cv2.imread(path, 0)
    # threshold
    th, threshed = cv2.threshold(gray, 100, 255,
                                 cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # findcontours
    cnts = cv2.findContours(threshed, cv2.RETR_LIST,
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

find_coords(path)