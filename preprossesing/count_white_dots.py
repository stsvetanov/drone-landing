import cv2

# path = "white dot.png"
path = "../images/white-dot.png"

# reading the image in grayscale mode
gray = cv2.imread(path, 0)

# show image
# cv2.imshow('image', gray)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# threshold
th, threshed = cv2.threshold(gray, 100, 255,
                             cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# findcontours
cnts = cv2.findContours(threshed, cv2.RETR_LIST,
                        cv2.CHAIN_APPROX_SIMPLE)[0]

# filter by area
s1 = 3
s2 = 20
xcnts = []

for cnt in cnts:
    if s1 < cv2.contourArea(cnt) < s2:
        xcnts.append(cnt)

    # printing output
print("\nDots number: {}".format(len(xcnts)))