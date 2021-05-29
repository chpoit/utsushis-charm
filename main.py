from src.__main__ import main
from src.arg_builder import build_args

if __name__ == "__main__":
    args = build_args()
    main(args)

