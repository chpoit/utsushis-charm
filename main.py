from src.__main__ import main
import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--thirdparty', dest='license', action='store_true',
                    help='Show 3rd party licenses')

if __name__ == "__main__":
    args = parser.parse_args()
    if args.license:
        print("Third party licenses")
        for f in os.scandir(os.path.join("LICENSES")):
            print(f"License for {f.name}")
            with open(f.path, "w"):
                print(f.read())

            print("\n\n")
    else:
        main()