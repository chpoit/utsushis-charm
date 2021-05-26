import os
import sys
from .frame_extraction import extract_unique_frames
from .charm_extraction import extract_charms, save_charms
from .charm_encoding import encode_charms
from .arg_builder import build_args
from .utils import print_licenses
import logging

logging.basicConfig(
    filename="app.log", filemode="w", format="%(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main(args):
    if args.license:
        print_licenses()
        sys.exit(0)

    input_dir = args.input_dir
    frame_dir = args.frame_dir
    charm_json = args.charm_json
    charm_encoded = args.charm_encoded

    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(frame_dir, exist_ok=True)

    if not args.skip_frames:
        extract_unique_frames(input_dir, frame_dir)

    if not args.skip_charms:
        charms = extract_charms(frame_dir)

        save_charms(charms, charm_json)
        print(f"Saved {len(charms)} charms")

    print("Encoding charms")
    encode_charms(charm_json, charm_encoded)
    print(
        'Charms encoded under "charms.encoded.txt". Use the contents of that file on the MHR Wiki armor set builder'
    )


if __name__ == "__main__":
    try:
        args = build_args()
        main(args)
    except Exception as e:
        logger.error(f"Crashed with {e}")
