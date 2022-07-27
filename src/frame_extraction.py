import os
import random
import cv2

from .utils import (
    apply_pre_crop_mask,
    get_frame_change_observation_section,
    compare_pixel,
)
from tqdm import tqdm
from math import floor
from skimage.metrics import structural_similarity
import numpy as np


def crop_frame(frame):
    x = 620
    y = 175
    x2 = x + 630
    y2 = y + 440
    pre_crop = apply_pre_crop_mask(frame)
    cropped = pre_crop[y:y2, x:x2]
    charm_only = get_frame_change_observation_section(cropped)
    return cropped, charm_only


def resize_to_16_9(frame):
    known_drops = [(1280, 720), (1920, 1080), (2560, 1440), (3840, 2160)]
    height, width = frame.shape[:2]

    ratio = round(width / height, 1)
    if ratio != 1.7 and ratio != 1.8:
        valid_drops = list(
            filter(lambda x: x[0] <= width and x[1] <= height, known_drops)
        )
        best_drop = valid_drops[-1]

        if height > best_drop[1]:
            odd_ratio = height / best_drop[1]
            tW = width / odd_ratio
            frame = cv2.resize(frame, [round(tW), best_drop[1]])

        height, width = frame.shape[:2]
        wCrop = floor((width - best_drop[0]) / 2)
        hCrop = floor((height - best_drop[1]) / 2)

        x = wCrop
        x2 = width - wCrop
        y = hCrop
        y2 = height - hCrop
        frame = frame[y:y2, x:x2]

    return frame


def resize_frame(frame):
    height, width = frame.shape[:2]
    if height != 720 or width != 1280:
        frame = cv2.resize(frame, (1280, 720))
    return frame


def crop_frames(capture_device, remove_black_bars, _=lambda x: x):
    for i, f in read_frames(capture_device, remove_black_bars, _):
        yield i, crop_frame(f)


def _jitter_pos(pos: int, jitter_range: int = 10):
    return pos + (random.randint(-jitter_range, jitter_range))


# top, left, right, bottom
def detect_black_bars(frame):
    height, width = frame.shape[:2]

    x_pos_base = floor(width / 2)
    y_pos_base = floor(height / 2)
    prev_pixel = None

    top = 5
    left = 5
    right = 5
    bottom = 5
    while True:
        pixel = frame[top, _jitter_pos(x_pos_base)]
        if prev_pixel is not None:
            if compare_pixel(pixel, prev_pixel):
                top += 1
            else:
                prev_pixel = None
                break
        else:
            prev_pixel = pixel

    while True:
        pixel = frame[height - bottom - 1, _jitter_pos(x_pos_base)]
        if prev_pixel is not None:
            if compare_pixel(pixel, prev_pixel):
                bottom += 1
            else:
                prev_pixel = None
                break
        else:
            prev_pixel = pixel

    while True:
        pixel = frame[_jitter_pos(y_pos_base), left]
        if prev_pixel is not None:
            if compare_pixel(pixel, prev_pixel):
                left += 1
            else:
                prev_pixel = None
                break
        else:
            prev_pixel = pixel

    while True:
        pixel = frame[_jitter_pos(y_pos_base), width - right - 1]
        if prev_pixel is not None:
            if compare_pixel(pixel, prev_pixel):
                right += 1
            else:
                prev_pixel = None
                break
        else:
            prev_pixel = pixel

    if top == 5:
        top = 0
    if left == 5:
        left = 0
    if right == 5:
        right = 0
    if bottom == 5:
        bottom = 0

    return (top, left, right, bottom)


def crop_black_bars(frame, black_bars):
    (top, left, right, bottom) = black_bars
    height, width = frame.shape[:2]

    y = top
    y2 = height - bottom
    x = left
    x2 = width - right
    return frame[y:y2, x:x2]


def read_frames(capture_device, remove_black_bars=False, _=lambda x: x):
    i = 0
    fps = capture_device.get(cv2.CAP_PROP_FPS)
    black_bars = None

    while True:
        ret, frame = capture_device.read()

        if not ret:
            break

        height, width = frame.shape[:2]
        ratio = round(width / height, 1)

        if ratio != 1.7 and ratio != 1.8:
            if i == 0:
                print(_("non-16:9"))
            frame = resize_to_16_9(frame)
        if i == 0:
            black_bars = detect_black_bars(frame)
        if fps == 60 and (i % 2):
            pass
        else:
            if remove_black_bars:
                frame = crop_black_bars(frame, black_bars)
            yield i, resize_frame(frame)

        i += 1


def is_new_frame(previous_charm_marker, charm_only):
    diff = cv2.absdiff(previous_charm_marker, charm_only)
    ret, threshold = cv2.threshold(diff, 60, 255, cv2.THRESH_BINARY_INV)

    return (
        0
        in threshold[
            :,
        ]
    )


def is_validated_video_format(video_name):
    return os.path.splitext(video_name)[-1] in [".mp4", ".mkv", ".avi", ".ogv", ".flv"]


def extract_unique_frames(
    input_dir,
    frame_dir,
    remove_black_bars=False,
    _=lambda x: x,
    iter_wrapper=None,
    frame_callback=lambda x: None,
):
    if not iter_wrapper:
        iter_wrapper = tqdm

    frame_count = 0
    current_frame = 0
    seq_count = 0

    input_files = list(
        filter(lambda x: is_validated_video_format(x.name), os.scandir(input_dir))
    )
    print(_("total-input").format(len(input_files)))

    frame_callback({"total_files": len(input_files), "current_file": 0})

    all_unique_frames = []

    for file_no, f_loc in enumerate(input_files):
        f_name = f_loc.name
        f_loc = f_loc.path

        cap = cv2.VideoCapture(f_loc)
        frame_count = floor(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if cap.get(cv2.CAP_PROP_FPS) == 60:
            print(_("60-fps"))
            frame_count = floor(frame_count / 2)

        frame_callback({"f_name": f_name, "frame_count": frame_count})

        previous_charm_marker = None
        with iter_wrapper(
            crop_frames(cap, remove_black_bars, _),
            total=frame_count,
            desc=_("fn-total-charm").format(f_name, frame_count),
        ) as frame_pbar:
            for i, cropped_tuple in frame_pbar:
                cropped, charm_only = cropped_tuple

                if previous_charm_marker is not None:
                    if is_new_frame(previous_charm_marker, charm_only):
                        seq_count += 1
                        all_unique_frames.append((current_frame, cropped, charm_only))
                else:
                    seq_count += 1
                    all_unique_frames.append((current_frame, cropped, charm_only))

                previous_charm_marker = charm_only

                frame_pbar.set_description(
                    _("fn-total-charm").format(f_name, current_frame)
                )
                current_frame += 1

                frame_callback(
                    {
                        "frame_count": frame_count,
                        "current_frame": current_frame,
                        "seq": seq_count,
                    }
                )

        cap.release()
        cv2.destroyAllWindows()

        frame_callback({"file_no": file_no})

    frame_callback({"f_name": _("done-scanning")})

    non_seq = 0
    with iter_wrapper(range(len(all_unique_frames)), desc=_("detect-non-seq")) as pbar:
        for i in pbar:
            is_new = True
            sourceNo, sourceCrop, sourceCharmOnly = all_unique_frames[i]
            for j in range(i + 1, len(all_unique_frames)):
                _unused, cropped, charm_only = all_unique_frames[j]
                is_new = is_new_frame(sourceCharmOnly, charm_only)
                if not is_new:
                    break
            if is_new:
                non_seq += 1
                name = os.path.join(frame_dir, f"frame{sourceNo}.png")
                cv2.imwrite(name, sourceCrop)

            frame_callback({"non_seq": non_seq})

    print(_("non-seq-diff").format(frame_count, non_seq))


if __name__ == "__main__":
    input_dir = "inputs"
    frame_dir = "frames"
    os.makedirs(frame_dir, exist_ok=True)
    extract_unique_frames(input_dir, frame_dir)
