import os
import json
from .frame_extraction import extract_unique_frames
from .charm_extraction import extract_charms, save_charms
from .charm_encoding import encode_charms
from .arg_builder import build_args
from .utils import print_licenses
import logging

logging.basicConfig(filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def main(args):
    if args.license:
        print_licenses()
        exit()

    input_dir = "inputs"
    frame_dir = "frames"
    charm_json = "charms.json"

    for d in [input_dir, frame_dir]:
        os.makedirs(d, exist_ok=True)

    # extract_unique_frames(input_dir, frame_dir)

    charms = extract_charms(frame_dir)

    save_charms(charms, charm_json)
    print(f"Saved {len(charms)} charms")

    print("Encoding charms")
    encode_charms(charm_json)
    print("Charms encoded under \"charms.encoded.txt\". Use the contents of that file on the MHR Wiki armor set builder")


if __name__ == "__main__":
    try:
        args = build_args()
        main(args)
    except Exception as e:
        logger.error(f"Crashed with {e}")
