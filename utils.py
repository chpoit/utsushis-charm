import os
import cv2
import numpy as np


def get_charm_borders(img):
    hsv = [0, 179, 0, 255, 1, 255]
    charm_only_filter_path = os.path.join("images","charm_only_white.png")
    charm_only_filter = cv2.imread(charm_only_filter_path)

    lower = np.array([hsv[0], hsv[2], hsv[4]])
    upper = np.array([hsv[1], hsv[3], hsv[5]])

    mask = cv2.inRange(charm_only_filter, lower, upper)

    return cv2.bitwise_or(img, img, mask=mask)


def get_charms_only(img):
    hsv = [0, 179, 0, 255, 1, 255]
    charm_only_filter_path = os.path.join("images","charm_only_white.png")
    charm_only_filter = cv2.imread(charm_only_filter_path)

    lower = np.array([hsv[0], hsv[2], hsv[4]])
    upper = np.array([hsv[1], hsv[3], hsv[5]])

    mask = cv2.inRange(img, lower, upper)

    return cv2.bitwise_and(img, charm_only_filter, mask=mask)


def only_keep_shiny_border(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv = [0, 39, 0, 255, 109, 255]

    lower = np.array([hsv[0], hsv[2], hsv[4]])
    upper = np.array([hsv[1], hsv[3], hsv[5]])

    mask = cv2.inRange(imgHSV, lower, upper)
    imgResult = cv2.bitwise_and(img, img, mask=mask)

    ret, imgResult = cv2.threshold(imgResult, 50, 255, cv2.THRESH_BINARY)
    return imgResult


def stackImages(scale, imgArray):

    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(
                        imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(
                        imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(
                        imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(
                    imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(
                    imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver
