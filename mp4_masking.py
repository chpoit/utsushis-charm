import os
import ffmpeg

os.makedirs("masked", exist_ok=True)


def create_masks(input_dir):
    overlay_file = ffmpeg.input('mask.png')

    for f_loc in os.scandir(input_dir):
        if not f_loc.name.endswith(".mp4"):
            continue
        print(f_loc.name)

        f_loc = f_loc.path
        f_out = f_loc.replace(".mp4", ".masked.mp4").replace(
            "inputs", "masked")

        (
            ffmpeg
            .input(f_loc)
            .overlay(overlay_file)
            .crop(620, 175, 630, 440)
            .output(f_out)
            .overwrite_output()
            .run()
        )
        # command = f"ffmpeg -i {f_loc} -i mask.png -filter_complex \"[0:v][1:v] overlay=0:0:enable='between(t,0,20)'\" -pix_fmt yuv420p -c:a copy {f_out}"

        # os.system(command)


if __name__ == "__main__":
    input_dir = "inputs"
    create_masks(input_dir)
