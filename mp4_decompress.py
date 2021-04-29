import cv2
import numpy as np
import os
from utils import *


#C:\Users\chpoit\AppData\Local\Tesseract-OCR
frame_dir = "unique_frames"

os.makedirs("unique_frames", exist_ok=True)

found_charms = {}

currentFrame = 0
for f_loc in os.scandir("masked"):
    if not f_loc.name.endswith(".masked.mp4"):
        continue
    print(f_loc.name)

    f_loc = f_loc.path
    cap = cv2.VideoCapture(f_loc)
    
    while(True):
        ret, frame = cap.read()
        if not ret:
            break
        currentFrame += 1
        # frameHSV = 
        color = (137,116,75)
        hsv =[10, 52, 64, 120, 106, 194]
        name = os.path.join(frame_dir, f"frame{currentFrame}.png")

        detectColor(frame, hsv)
        # cv2.imshow('FRAME', frame)
        cv2.waitKey(0)
        exit()
        # print(currentFrame)


        cv2.imwrite(name, frame)

    cap.release()
    cv2.destroyAllWindows()




