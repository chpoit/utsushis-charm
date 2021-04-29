# 547,26 - 628,51
# 27*26

# Skill name size 216*21
# Skill 1: 413, 94
# Skill 2: 413, 144
# Skill 3: 413, 194

# Level Size: 12 * 21
# Level 1: 618, 117
# Level 2: 618, 167
# Level 3: 618, 217

# C:\Users\chpoit\AppData\Local\Tesseract-OCR

import os
import numpy as np

from utils import *

frame_dir = "unique_frames"

for frame_loc in os.scandir(frame_dir):
    frame_loc = frame_loc.path
