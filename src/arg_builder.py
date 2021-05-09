import argparse

def build_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--thirdparty', dest='license', action='store_true',
                    help='Show 3rd party licenses')
    parser.add_argument('--skip-frames', dest='skip_frames', action='store_true',
                    help='Show 3rd party licenses')
    parser.add_argument('--skip-charms', dest='skip_charms', action='store_true',
                    help='Show 3rd party licenses')

    parser.add_argument("-i", "--input", dest="input_dir", required=False,
                    help="Input directory for videos", default='inputs')
    parser.add_argument("-f", "--frames", dest="frame_dir", required=False,
                    help="Directory to store temporary frames", default='frames')
    
    return parser.parse_args()