import cv2

# path = "white dot.png"
path = "../images/multiple-blob-inv.png"

# reading the image in grayscale mode
img = cv2.imread(path, 0)
# gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# show image
# cv2.imshow('image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# threshold
# th, threshed = cv2.threshold(img, 50, 255,
#                              cv2.THRESH_BINARY | cv2.THRESH_OTSU)
th,threshed = cv2.threshold(img, 127, 255, 0)

# findcontours
contours = cv2.findContours(threshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]

# printing output
print("\nDots number: {}".format(len(contours)))

for contour in contours:
    # calculate moments for each contour
    M = cv2.moments(contour)

    # calculate x,y coordinate of center
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])