from src.__main__ import main
import os
import sys
from src.arg_builder import build_args
import multiprocessing

if __name__ == "__main__":
    multiprocessing.freeze_support()
    args = build_args()
    main(args)

    input("Press Enter to Exit...")
