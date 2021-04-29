import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\chpoit\\AppData\\Local\\Tesseract-OCR\\tesseract.exe"


def get_charm_borders(img):
    hsv = [0, 179, 0, 255, 1, 255]
    charm_only_filter_path = os.path.join("images", "charm_only_white.png")
    charm_only_filter = cv2.imread(charm_only_filter_path)

    lower = np.array([hsv[0], hsv[2], hsv[4]])
    upper = np.array([hsv[1], hsv[3], hsv[5]])

    mask = cv2.inRange(charm_only_filter, lower, upper)

    return cv2.bitwise_or(img, img, mask=mask)


def get_charms_only(img):
    hsv = [0, 179, 0, 255, 1, 255]
    charm_only_filter_path = os.path.join("images", "charm_only_white.png")
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

    
def filter_text_skill(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv = [0, 179, 0, 16, 85, 255]

    lower = np.array([hsv[0], hsv[2], hsv[4]])
    upper = np.array([hsv[1], hsv[3], hsv[5]])

    mask = cv2.inRange(imgHSV, lower, upper)
    imgResult = cv2.bitwise_and(img, img, mask=mask)

    ret, imgResult = cv2.threshold(imgResult, 50, 255, cv2.THRESH_BINARY)
    return imgResult

def filter_text_skill_v2(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv = [0, 179, 0, 16, 142, 255]

    lower = np.array([hsv[0], hsv[2], hsv[4]])
    upper = np.array([hsv[1], hsv[3], hsv[5]])

    mask = cv2.inRange(imgHSV, lower, upper)
    imgResult = cv2.bitwise_and(img, img, mask=mask)

    ret, imgResult = cv2.threshold(imgResult, 50, 255, cv2.THRESH_BINARY)
    return imgResult


def remove_non_skill_info(img):
    hsv = [0, 179, 0, 255, 142, 255]
    skill_only_path = os.path.join("images", "skill_mask.png")
    skill_filter = cv2.imread(skill_only_path)

    lower = np.array([hsv[0], hsv[2], hsv[4]])
    upper = np.array([hsv[1], hsv[3], hsv[5]])

    imgHSV = cv2.cvtColor(skill_filter, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV, lower, upper)

    imgResult = cv2.bitwise_and(img, img, mask=mask)

    return imgResult


def extract_grayscale_threshold(img, bottom_thresh=85, top_thresh=255):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, th3 = cv2.threshold(
        gray, bottom_thresh, top_thresh, cv2.THRESH_BINARY)

    # th3 = cv2.adaptiveThreshold(gray,200,cv2.ADAPTIVE_THRESH_MEAN_C,\
    #         cv2.THRESH_BINARY,11,2)

    # th3 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #         cv2.THRESH_BINARY,11,2)

    return th3

def read_text_from_skill_tuple(skills):
    skill_text =[]
    for skill_img, level_img in skills:
        skill = pytesseract.image_to_string(skill_img)
        level = getNumber(level_img)
        skill_text.append((skill, level))
    
    return skill_text
    
def getNumber(image):
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    except:
        gray = image
    # Otsu Tresholding automatically find best threshold value
    _, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    
    # invert the image if the text is white and background is black
    count_white = np.sum(binary_image > 0)
    count_black = np.sum(binary_image == 0)
    if count_black > count_white:
        binary_image = 255 - binary_image
        
    # padding
    final_image = cv2.copyMakeBorder(image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    txt = pytesseract.image_to_string(
        final_image, config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')

    return txt


def get_slots(img):
    w = 27
    h = 26
    y = 26

    x1 = 547
    x2 = x1 + w+1
    x3 = x1 + w*2+1

    slot0 = cv2.imread(os.path.join("images", "slot0.png"))
    slot1 = cv2.imread(os.path.join("images", "slot1.png"))
    slot2 = cv2.imread(os.path.join("images", "slot2.png"))
    slot3 = cv2.imread(os.path.join("images", "slot3.png"))

    spot1 = img[y:y + h, x1:x1 + w]
    spot2 = img[y:y + h, x2:x2 + w]
    spot3 = img[y:y + h, x3:x3 + w]

    slots = []
    most_similar = None
    j = 1
    for spot in [spot1, spot2, spot3]:
        score0 = structural_similarity(spot, slot0, multichannel=True)
        score1 = structural_similarity(spot, slot1, multichannel=True)
        score2 = structural_similarity(spot, slot2, multichannel=True)
        score3 = structural_similarity(spot, slot3, multichannel=True)

        j+=1
        scores = [score0, score1, score2, score3]
        best = max(scores)
        for i,s in enumerate(scores):
            if s == best:
                slots.append(i)
                if i==0: break

    slots+=[0]*3
    return slots[:3]

def get_skills(img):
    skills = _get_skills(img)
    levels = _get_levels(img)

    return list(zip(skills, levels))

def _get_skills(img):
    w = 216
    h = 21
    x = 413

    y1 = 94
    y2 = 144

    skill1 = img[y1:y1 + h, x:x + w]
    skill2 = img[y2:y2 + h, x:x + w]
    
    return skill1, skill2

def _get_levels(img):
    w = 12
    h = 21
    x = 618

    y1 = 117
    y2 = 167

    level1 = img[y1:y1 + h, x:x + w]
    level2 = img[y2:y2 + h, x:x + w]

    return level1, level2



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
