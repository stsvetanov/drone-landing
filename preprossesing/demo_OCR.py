import cv2
import pytesseract as pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Load an color image in color
img = cv2.imread('../images/Tales-at-Night-010.jpg', cv2.IMREAD_COLOR)
# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# blurred = cv2.GaussianBlur(gray, (9, 9), 0)
ret, thresh = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY_INV)

text = pytesseract.image_to_string(img, config='--psm 11', lang="bul")
print(text)

cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
