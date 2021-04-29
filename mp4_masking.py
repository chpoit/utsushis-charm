import os
import ffmpeg


def create_masks(input_dir, masked_dir):
    overlay_file = ffmpeg.input(os.path.join('images', 'mask.png'))

    for f_loc in os.scandir(input_dir):
        if not f_loc.name.endswith(".mp4"):
            continue
        print(f_loc.name)

        f_loc = f_loc.path
        f_out = f_loc.replace(".mp4", ".masked.mp4").replace(
            input_dir, masked_dir)

        (
            ffmpeg
            .input(f_loc)
            .overlay(overlay_file)
            .crop(620, 175, 630, 440)
            .output(f_out)
            .overwrite_output()
            .run()
        )


if __name__ == "__main__":
    input_dir = "inputs"
    masked_dir = "masked"
    os.makedirs(masked_dir, exist_ok=True)
    create_masks(input_dir, masked_dir)
