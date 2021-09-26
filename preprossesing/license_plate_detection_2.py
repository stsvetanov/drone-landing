import cv2
import numpy as np
import pytesseract as pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
from scipy.spatial import distance as dist


def midpoint(ptA, ptB):
    return (int((ptA[0] + ptB[0]) * 0.5), int((ptA[1] + ptB[1]) * 0.5))

# Load an color image in grayscale
#img = cv2.imread('../images/plate.jpg', 0)

# Load an color image in color
img = cv2.imread('../images/plate2.jfif', cv2.IMREAD_COLOR)

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# blurred = cv2.GaussianBlur(gray, (3, 3), 0)
ret, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)

# edged = cv2.Canny(thresh, 30, 200) #Perform Edge detection
cnts = cv2.findContours(thresh, cv2.RETR_TREE,
                            cv2.CHAIN_APPROX_SIMPLE)[0]
s_min = 500
s_max = 100000
xcnts = []
coordinates = []

for cnt in cnts:
    if s_min < cv2.contourArea(cnt) < s_max:

        epsilon = 0.05 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True);
        # cv2.drawContours(img, approx, -1, (0, 255, 0), 6)

        if len(approx) == 4:
            sizes = []
            for i in range(-3, 1):
                cv2.line(img, tuple(approx[i - 1][0]), tuple(approx[i][0]), (0, 255, 100), 4)
                size = dist.euclidean(tuple(approx[i - 1][0]), tuple(approx[i][0]))
                # position = midpoint(tuple(approx[i - 1][0]), tuple(approx[i][0]))
                # cv2.putText(img, f"{round(size, 1)}", position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3, cv2.LINE_AA)
                sizes.append(size)
            if abs(sizes[0] / sizes[2]) > 0.9 and abs(sizes[1] / sizes[3]) > 0.9:
                screenCnt = approx
                break
# Masking the part other than the number plate
mask = np.zeros(thresh.shape, np.uint8)
new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
new_image = cv2.bitwise_and(thresh, thresh, mask=mask)

# Now crop
(x, y) = np.where(mask == 255)
(topx, topy) = (np.min(x), np.min(y))
(bottomx, bottomy) = (np.max(x), np.max(y))
cropped = new_image[topx:bottomx+1, topy:bottomy+1]

        # xcnts.append(cnt)
        # M = cv2.moments(cnt)
        #
        # # calculate x,y coordinate of center
        # cX = int(M["m10"] / M["m00"])
        # cY = int(M["m01"] / M["m00"])
        # # if plate_dots[0][0] < cX < plate_dots [3][0] and plate_dots[0][1] < cY < plate_dots [3][1]:
        # cv2.circle(img, (cX, cY), 15, (0, 255, 0), -1)
        #
        # coordinates.append((cX, cY))

# Rotation
# rows, cols = cropped.shape
# M = cv2.getRotationMatrix2D((cols/2, rows/2), 15, 1)
# dst = cv2.warpAffine(cropped, M, (cols,rows))

text = pytesseract.image_to_string(cropped, config='--psm 11')
print("Detected Number is:", text)

cv2.imshow('image', cropped)
# cv2.imwrite('dst.jpg', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
