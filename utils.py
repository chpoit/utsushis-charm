import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity
import pytesseract


def get_charm_borders(img):
    hsv = [0, 179, 0, 255, 1, 255]
    charm_only_filter_path = os.path.join("images", "charm_only.png")
    charm_only_filter = cv2.imread(charm_only_filter_path)

    lower = np.array([hsv[0], hsv[2], hsv[4]])
    upper = np.array([hsv[1], hsv[3], hsv[5]])

    mask = cv2.inRange(charm_only_filter, lower, upper)

    return cv2.bitwise_or(img, img, mask=mask)


def get_charms_only(img):
    hsv = [0, 179, 0, 255, 1, 255]
    charm_only_filter_path = os.path.join("images", "charm_only.png")
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


def silly_double_threshold(img):
    # 203 255 135 255
    ret, thresh3 = cv2.threshold(img, 203, 255, cv2.THRESH_TRUNC)
    ret, thresh35 = cv2.threshold(thresh3, 135, 255, cv2.THRESH_BINARY)
    return cv2.cvtColor(thresh35, cv2.COLOR_BGR2GRAY)


def silly_trunc_threshold(img):
    ret, thresh3 = cv2.threshold(img, 203, 255, cv2.THRESH_TRUNC)
    return thresh3


def read_text_from_skill_tuple(skills):
    skill_text = []
    for skill_img, level in skills:
        skill = pytesseract.image_to_string(skill_img,
                                            config="-c tessedit_char_whitelist=-/ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
        skill_text.append((skill, level))

    return skill_text


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

        j += 1
        scores = [score0, score1, score2, score3]
        best = max(scores)
        for i, s in enumerate(scores):
            if s == best:
                slots.append(i)
                if i == 0:
                    break

    slots += [0]*3
    return slots[:3]


def get_skills(img, inverted=False):
    def _has_level(x):
        x, y = x
        return y > 0
    skills = _get_skills(img)
    levels = _get_levels(img, inverted=inverted)

    return list(filter(_has_level, zip(skills, levels)))


def _get_skills(img):
    w = 216
    h = 23
    x = 413

    y1 = 92
    y2 = 142

    skill1 = img[y1:y1 + h, x:x + w]
    skill2 = img[y2:y2 + h, x:x + w]

    return skill1, skill2


def _get_levels(img, inverted=False):
    w = 12
    h = 21
    x = 618

    y1 = 117
    y2 = 167

    lv1 = cv2.imread(os.path.join("images", "lv1.png"), 0)
    lv2 = cv2.imread(os.path.join("images", "lv2.png"), 0)
    lv3 = cv2.imread(os.path.join("images", "lv3.png"), 0)

    level1 = img[y1:y1 + h, x:x + w]
    level2 = img[y2:y2 + h, x:x + w]
    if inverted:
        level1 = cv2.bitwise_not(level1)
        level2 = cv2.bitwise_not(level2)

    levels = []
    for level in [level1, level2]:
        try:
            gs = cv2.cvtColor(level, cv2.COLOR_BGR2GRAY)
        except:
            gs =level
        score1 = structural_similarity(gs, lv1)
        score2 = structural_similarity(gs, lv2)
        score3 = structural_similarity(gs, lv3)

        scores = [score1, score2, score3]
        best = max(scores)
        if best < 0.5:
            levels.append(0)
            continue
        for i, s in enumerate(scores):
            if s == best:
                levels.append(i+1)

    return levels
