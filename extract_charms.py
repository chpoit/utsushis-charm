# 547,26 - 628,51
# 27*26

# Skill name size 216*21
# Skill 1: 413, 94
# Skill 2: 413, 144
# Skill 3: 413, 194 -> Jewels were not removed

# Level Size: 12 * 21
# Level 1: 618, 117
# Level 2: 618, 167
# Level 3: 618, 217 -> Jewels were not removed

# C:\Users\chpoit\AppData\Local\Tesseract-OCR

import os
import cv2
import numpy as np

from utils import *

def show_mess(mess):
    t = []
    t2 =[]
    for s, l in mess:
        t.append([s])
        t2.append([l])
    
    stacked = stackImages(1, t)
    stacked2 = stackImages(4, t2)
    cv2.imshow("mess",stacked)
    cv2.imshow("mess2",stacked2)
    # cv2.imwrite("mess.png", stacked)

frame_dir = "unique_frames"

for frame_loc in os.scandir(frame_dir):
    frame_loc = frame_loc.path
    frame = cv2.imread(frame_loc)
    skill_only = remove_non_skill_info(frame)

    skills = get_skills(skill_only)

    slots = get_slots(skill_only)

    print(slots)
    skill_text = read_text_from_skill_tuple(skills)
    # skill_text = read_text_from_skill_tuple(mess)
    
    for skill, level in skill_text:
        print(skill.strip(), level.strip())

    # cv2.imshow("Stacked",stacked)
    cv2.imshow("skillz",skill_only)
    cv2.waitKey(0)
    exit()

