import argparse


def build_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--console", dest="console", action="store_true", help="Runs in console mode"
    )

    parser.add_argument(
        "--thirdparty",
        dest="license",
        action="store_true",
        help="Shows 3rd party licenses",
    )

    parser.add_argument(
        "--skip-frames",
        dest="skip_frames",
        action="store_true",
        help="Skips the first frame extraction step. Useful if the second step crashed.",
    )
    parser.add_argument(
        "--skip-charms",
        dest="skip_charms",
        action="store_true",
        help="Skips the Tesseract-OCR step. Not sure why you would want that.",
    )

    parser.add_argument(
        "-i",
        "--input",
        dest="input_dir",
        required=False,
        help="Changes the Input directory for videos",
        default="inputs",
    )
    parser.add_argument(
        "-f",
        "--frames",
        dest="frame_dir",
        required=False,
        help="Changes the Directory used to store temporary frames",
        default="frames",
    )

    parser.add_argument(
        "-c",
        "--charm-json",
        dest="charm_json",
        required=False,
        help="Changes the name of the json formatted charms",
        default="charms.json",
    )
    parser.add_argument(
        "-e",
        "--charm-encoded",
        dest="charm_encoded",
        required=False,
        help="Changes the name of the MHR-Wiki formatted charms",
        default="charms.encoded.txt",
    )

    parser.add_argument(
        "-l",
        "--language",
        dest="language",
        required=False,
        help="Sets the language of the switch recording.",
        default="English",
    )

    parser.add_argument(
        "-a",
        "--app-language",
        dest="app_language",
        required=False,
        help="Sets the language of the switch recording.",
        default="English",
    )

    parser.add_argument(
        "--autoexit",
        dest="autoexit",
        action="store_true",
        help='Skips the "Press enter to exit" prompt in console mode.',
    )

    return parser.parse_args()
