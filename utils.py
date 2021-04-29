import cv2
import numpy as np

def detectColor(img, hsv):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # cv2.imshow("hsv",imgHSV)
    lower = np.array([hsv[0], hsv[2], hsv[4]])
    upper = np.array([hsv[1], hsv[3], hsv[5]])
    mask = cv2.inRange(imgHSV, lower, upper)
    # cv2.imshow("mask", mask)
    imgResult = cv2.bitwise_and(img, img, mask=mask)
    cv2.imshow("imgResult", imgResult)
    return imgResult