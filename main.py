import os
from mp4_masking import create_masks
from mp4_decompress import extract_unique_frames
from extract_charm import extract_charms, save_charms


if __name__ == "__main__":

    input_dir = "inputs"
    masked_dir = "masked"
    frame_dir = "unique_frames"
    charm_json = "charms.json"

    for d in [input_dir, masked_dir,frame_dir]:
        os.makedirs(d, exist_ok=True)

    create_masks(input_dir, masked_dir)

    extract_unique_frames(masked_dir, frame_dir)

    charms = extract_charms(frame_dir)

    save_charms(charms)
    print(f"Saved {len(charms)} charms")
