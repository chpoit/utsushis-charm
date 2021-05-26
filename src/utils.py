import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity
from math import floor
from .tesseract.tesseract_utils import process_image_with_tesseract


def _load_potentially_transparent(filename):
    pot_transparent = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    trans_mask = pot_transparent[:, :, 3] == 0
    pot_transparent[trans_mask] = [255, 255, 255, 255]
    return cv2.cvtColor(pot_transparent, cv2.COLOR_BGRA2BGR)


def apply_black_white_mask(img, mask_img):
    lower = np.array([1]*3)
    upper = np.array([255]*3)
    mask = cv2.inRange(mask_img, lower, upper)

    return cv2.bitwise_and(img, img, mask=mask)


def apply_pre_crop_mask(img):
    pre_crop_filter = _load_potentially_transparent(get_resource_path("mask"))
    return apply_black_white_mask(img, pre_crop_filter)


def get_frame_change_observation_section(img):
    charm_only_filter_path = get_resource_path("charm_only")
    charm_only_filter = cv2.imread(charm_only_filter_path)
    charm_only = apply_black_white_mask(img, charm_only_filter)
    return cv2.cvtColor(charm_only[185:424, 15:370], cv2.COLOR_BGR2GRAY)


def remove_non_skill_info(img):
    skill_only_path = get_resource_path("skill_mask")
    skill_filter = cv2.imread(skill_only_path)
    skill_only = apply_black_white_mask(img, skill_filter)
    return skill_only


def apply_trunc_threshold(img):
    ret, thresholded = cv2.threshold(img, 203, 255, cv2.THRESH_TRUNC)
    return thresholded


def _trim_image_past_skill_name(img, background_color=203):
    shape = img.shape
    empty_col = 0
    i = floor(shape[0]/2)
    for j in range(shape[1]):
        if len(shape) == 3:
            pixel = img[i][j][0]
        else:
            pixel = img[i][j]

        if pixel != background_color:
            empty_col = -1

        empty_col += 1
        if empty_col >= 15:
            break

    trimmed = img[:, :j-10] if len(shape) != 3 else img[:, :j-10, :]
    return trimmed


def read_text_from_skill_tuple(tess, skills):
    skill_text = []
    for skill_img, level in skills:
        skill_img = _trim_image_past_skill_name(skill_img)
        skill = process_image_with_tesseract(tess, skill_img)
        skill_text.append((skill, level))

    return skill_text


def get_slots(img):
    w = 27
    h = 26
    y = 26

    x1 = 547
    x2 = x1 + w+1
    x3 = x1 + w*2+1

    slot0 = cv2.imread(get_resource_path('slot0'))
    slot1 = cv2.imread(get_resource_path('slot1'))
    slot2 = cv2.imread(get_resource_path('slot2'))
    slot3 = cv2.imread(get_resource_path('slot3'))

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

    lv1 = cv2.imread(get_resource_path('lv1'), 0)
    lv2 = cv2.imread(get_resource_path('lv2'), 0)
    lv3 = cv2.imread(get_resource_path('lv3'), 0)

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
            gs = level
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


def get_resource_path(resource):
    return _resources[resource] if resource in _resources else resource


def _alter_resource_path(relative_path):
    import sys
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def print_licenses():
    print("Third party licenses")
    for f in os.scandir(get_resource_path("licences")):
        print(f"License for {f.name}")
        with open(f.path, "r") as l_f:
            print(l_f.read())

        print("\n\n")


def batchify(lst, batch_size):
    return list(batchify_lazy(lst, batch_size))


def batchify_lazy(lst, batch_size):
    batch = []
    i = 0
    for item in lst:
        if i > batch_size:
            i = 0
            yield batch
            batch = []
        batch.append(item)
        i += 1
    yield batch


_resources = {
    'skill_dict': _alter_resource_path(os.path.join("data", "skill_dict.freq")),
    'skill_list': _alter_resource_path(os.path.join("data", "skill_list.txt")),
    'skill_corrections': "skill_corrections.csv",
    'lv1': _alter_resource_path(os.path.join("images", "levels", "lv1.png")),
    'lv2': _alter_resource_path(os.path.join("images", "levels", "lv2.png")),
    'lv3': _alter_resource_path(os.path.join("images", "levels", "lv3.png")),
    'slot0': _alter_resource_path(os.path.join("images", "slots", "slot0.png")),
    'slot1': _alter_resource_path(os.path.join("images", "slots", "slot1.png")),
    'slot2': _alter_resource_path(os.path.join("images", "slots", "slot2.png")),
    'slot3': _alter_resource_path(os.path.join("images", "slots", "slot3.png")),
    'mask': _alter_resource_path(os.path.join("images", "mask.png")),
    'charm_only': _alter_resource_path(os.path.join("images", "charm_only.png")),
    'skill_mask': _alter_resource_path(os.path.join("images", "skill_mask.png")),
    'licences': _alter_resource_path("LICENSES"),
    'TRANSLATIONS': _alter_resource_path(os.path.join("data", "translation")),
    'ICON': _alter_resource_path(os.path.join("media", "icon.ico")),
}
