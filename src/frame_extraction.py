import os
import cv2
from .utils import pre_crop_mask, get_frame_change_observation_section, get_resource_path
from tqdm import tqdm
from math import floor
from skimage.metrics import structural_similarity


def extract_unique_frames(input_dir, frame_dir):
    overlay_file_name = get_resource_path("mask")
    charm_count = 0
    currentFrame = 0

    input_files = list(
        filter(lambda x: x.name.endswith(".mp4"), os.scandir(input_dir)))
    print(f"Total input files to scan: {len(input_files)}")
    for f_loc in input_files:
        f_name = f_loc.name
        f_loc = f_loc.path

        cap = cv2.VideoCapture(f_loc)
        # 620, 175, 630, 440
        x = 620
        y = 175
        x2 = x+630
        y2 = y+440
        previous_charm_marker = None
        with tqdm(total=floor(cap.get(cv2.CAP_PROP_FRAME_COUNT)), desc=f"{f_name},  Total Estimated charms found: {charm_count}") as tqdm_iter:
            while(True):
                ret, frame = cap.read()
                if not ret:
                    break
                currentFrame += 1
                name = os.path.join(frame_dir, f"frame{currentFrame}.png")

                pre_crop = pre_crop_mask(frame, overlay_file_name)
                cropped = pre_crop[y:y2, x:x2]

                charm_only = get_frame_change_observation_section(cropped)
                
                if previous_charm_marker is not None:
                    score = structural_similarity(
                        previous_charm_marker, charm_only)
                    if score < 0.996:
                        charm_count += 1

                        cv2.imwrite(name, cropped)
                else:
                    charm_count += 1
                    cv2.imwrite(name, cropped)

                previous_charm_marker = charm_only

                tqdm_iter.set_description(
                    f"{f_name},  Total Estimated charms found: {charm_count}")
                tqdm_iter.update(1)

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    input_dir = "inputs"
    frame_dir = "frames"
    os.makedirs(frame_dir, exist_ok=True)
    extract_unique_frames(input_dir, frame_dir)
