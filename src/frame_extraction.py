import os
import cv2
from .utils import apply_pre_crop_mask, get_frame_change_observation_section, get_resource_path
from tqdm import tqdm
from math import floor
from skimage.metrics import structural_similarity
import numpy as np


def crop_frame(frame):
    x = 620
    y = 175
    x2 = x+630
    y2 = y+440
    pre_crop = apply_pre_crop_mask(frame)
    cropped = pre_crop[y:y2, x:x2]
    charm_only = get_frame_change_observation_section(cropped)
    return cropped, charm_only


def crop_frames(capture_device):
    results = []
    for i, f in read_frames(capture_device):
        yield i, crop_frame(f)


def read_frames(capture_device):
    i = 0
    while(True):
        ret, frame = capture_device.read()
        if not ret:
            break
        yield i, frame
        i += 1


def is_new_frame(previous_charm_marker, charm_only):
    diff = cv2.absdiff(previous_charm_marker, charm_only)
    ret, threshold = cv2.threshold(diff, 60, 255, cv2.THRESH_BINARY_INV)

    return 0 in threshold[:, ]


def extract_unique_frames(input_dir, frame_dir):
    charm_count = 0
    currentFrame = 0

    input_files = list(
        filter(lambda x: x.name.endswith(".mp4"), os.scandir(input_dir)))
    print(f"Total input files to scan: {len(input_files)}")

    all_unique_frames = []

    for f_loc in input_files:
        f_name = f_loc.name
        f_loc = f_loc.path

        cap = cv2.VideoCapture(f_loc)
        frame_count = floor(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        previous_charm_marker = None
        with tqdm(crop_frames(cap), total=frame_count, desc=f"{f_name},  Total Estimated charms/frames found: {charm_count}") as frame_pbar:
            for i, cropped_tuple in frame_pbar:
                cropped, charm_only = cropped_tuple

                if previous_charm_marker is not None:

                    if is_new_frame(previous_charm_marker, charm_only):
                        charm_count += 1
                        all_unique_frames.append(
                            (currentFrame, cropped, charm_only))
                else:
                    charm_count += 1
                    all_unique_frames.append(
                        (currentFrame, cropped, charm_only))

                previous_charm_marker = charm_only

                frame_pbar.set_description(
                    f"{f_name},  Total Estimated charms/frames found: {charm_count}")
                currentFrame += 1

        cap.release()
        cv2.destroyAllWindows()

    non_seq = 0
    for i in tqdm(range(len(all_unique_frames)), desc="Detecting non-sequential duplicate frames"):
        is_new = True
        sourceNo, sourceCrop, sourceCharmOnly = all_unique_frames[i]
        for j in range(i+1, len(all_unique_frames)):
            _, cropped, charm_only = all_unique_frames[j]            
            is_new = is_new_frame(sourceCharmOnly, charm_only)
            if not is_new:
                break
        if is_new:
            non_seq+=1
            name = os.path.join(frame_dir, f"frame{sourceNo}.png")
            cv2.imwrite(name, sourceCrop)
    
    print(f"Reduced frames from {charm_count} to {non_seq}")



if __name__ == "__main__":
    input_dir = "inputs"
    frame_dir = "frames"
    os.makedirs(frame_dir, exist_ok=True)
    extract_unique_frames(input_dir, frame_dir)
