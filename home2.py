import math

import cv2
import numpy as np

def deskew(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    (h, w) = thresh.shape
    moments = cv2.moments(thresh)
    if moments['m00'] == 0:
        return image
    x = int(moments['m10']/moments['m00'])
    y = int(moments['m01']/moments['m00'])

    angle = -(x - w/2) / (h/2 - y) * 180 / np.pi

    (h, w) = image.shape[:2]
    center = (w//2, h//2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    deskewed = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


    (h, w) = deskewed.shape[:2]
    left = int((w - w/math.cos(angle))/2)
    top = int((h - h/math.cos(angle))/2)
    right = int(left + w/math.cos(angle))
    bottom = int(top + h/math.cos(angle))

    deskewed = deskewed[top:bottom, left:right]

    return deskewed


image = cv2.imread(r"C:\Users\ssolwa001\Pictures\evan12.jpg")
image = deskew(image)
cv2.imwrite("deskewed.jpg", image)


