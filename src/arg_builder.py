import argparse

def build_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--thirdparty', dest='license', action='store_true',
                    help='Show 3rd party licenses')
    
    return parser.parse_args()