import cv2
from scipy.spatial import distance as dist


def midpoint(ptA, ptB):
    return (int((ptA[0] + ptB[0]) * 0.5), int((ptA[1] + ptB[1]) * 0.5))

# Load an color image in grayscale
# img = cv2.imread('images/multiple-blob.png', 0)

# Load an color image in color
# img = cv2.imread('images/multiple-blob.png', cv2.IMREAD_COLOR)
img = cv2.imread('images/plate.jpg', cv2.IMREAD_COLOR)
# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)
blurred = cv2.GaussianBlur(gray, (9, 9), 0)
ret, thresh = cv2.threshold(blurred, 130, 255, cv2.THRESH_BINARY_INV)

edged = cv2.Canny(thresh, 30, 200) #Perform Edge detection
cnts = cv2.findContours(thresh, cv2.RETR_TREE,
                            cv2.CHAIN_APPROX_SIMPLE)[0]
s_min = 150
s_max = 1000000
xcnts = []
coordinates = []

for cnt in cnts:
    if s_min < cv2.contourArea(cnt) < s_max:

        epsilon = 0.03 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True);
        cv2.drawContours(img, approx, -1, (0, 255, 0), 6)
        if len(approx) == 4:

            for i in range(-3, 1):
                cv2.line(img, tuple(approx[i - 1][0]), tuple(approx[i][0]), (0, 255, 100), 4)
                size = dist.euclidean(tuple(approx[i - 1][0]), tuple(approx[i][0]))
                position = midpoint(tuple(approx[i - 1][0]), tuple(approx[i][0]))
                cv2.putText(img, f"{round(size, 1)}", position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3,
                            cv2.LINE_AA)

        xcnts.append(cnt)
        M = cv2.moments(cnt)

        # calculate x,y coordinate of center
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(img, (cX, cY), 15, (0, 255, 0), -1)

        coordinates.append((cX, cY))

print(f"Dots number: {len(xcnts)}")
print(f"Coordinates: {coordinates}")

cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
