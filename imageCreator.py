import cv2
import os
import sys

image = cv2.imread(f'{os.getcwd()}/Images/{sys.argv[1]}', cv2.IMREAD_COLOR)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.blur(gray, (3, 3))

cv2.imwrite('Images/blurred_circle.png', img=blur)