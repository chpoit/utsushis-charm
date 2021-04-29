import cv2
import numpy as np
import os
from utils import *
from skimage.metrics import structural_similarity


def extract_unique_frames(masked_dir, frame_dir):
    currentFrame = 0
    charm_count = 0
    for f_loc in os.scandir(masked_dir):
        if not f_loc.name.endswith(".masked.mp4"):
            continue
        print(f_loc.name)

        f_loc = f_loc.path
        cap = cv2.VideoCapture(f_loc)

        previous_frame = None
        while(True):
            ret, frame = cap.read()
            if not ret:
                break
            currentFrame += 1
            name = os.path.join(frame_dir, f"frame{currentFrame}.png")

            charm_border = get_charm_borders(frame)
            shiny = only_keep_shiny_border(charm_border)

            if previous_frame is not None:
                shiny_grayscale = cv2.cvtColor(shiny, cv2.COLOR_BGR2GRAY)
                score = structural_similarity(previous_frame, shiny_grayscale)
                if score < 0.996:
                    charm_count += 1
                    print(
                        f"Saving frame {currentFrame}, Estimated charms found: {charm_count}")
                    cv2.imwrite(name, frame)
            else:
                cv2.imwrite(name, frame)
            previous_frame = cv2.cvtColor(shiny, cv2.COLOR_BGR2GRAY)

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    masked_dir = "masked"
    frame_dir = "unique_frames"
    os.makedirs(frame_dir, exist_ok=True)

    extract_unique_frames(masked_dir, frame_dir)
