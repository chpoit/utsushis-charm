from .TesseractError import TesseractError
import numpy as np
import os
import sys
import ctypes
import ctypes.util
import platform
from urllib import request
from tqdm import tqdm

import logging
from pathlib import Path

logger = logging.getLogger(__name__)
HOME = str(Path.home())
WINDOWS = platform.system() == "Windows"
LINUX = platform.system() == "Linux"
MAC = platform.system() == "Darwin"


def _is_pyinstaller():
    return hasattr(sys, "_MEIPASS")


def _get_pyinstaller_tesseract_path():
    base_path = sys._MEIPASS
    bundled_path = os.path.join(base_path, "Tesseract-OCR", "libtesseract-4.dll")
    return bundled_path


def find_tesseract():
    if _is_pyinstaller():
        print("Using bundled tesseract")
        return _get_pyinstaller_tesseract_path()

    # TODO: Make this resilient to "change" (tesseract version), probably not necessary
    locations = [
        ctypes.util.find_library("libtesseract-4"),  # win32
        ctypes.util.find_library("libtesseract302"),  # win32 version 3.2
        ctypes.util.find_library("tesseract"),  # others
    ]

    if WINDOWS:
        locations += [
            os.path.join(
                os.getenv("ProgramW6432"), "Tesseract-OCR", "libtesseract-4.dll"
            ),
            os.path.join(
                os.getenv("LOCALAPPDATA"), "Tesseract-OCR", "libtesseract-4.dll"
            ),
            os.path.join(
                os.getenv("ProgramFiles"), "Tesseract-OCR", "libtesseract-4.dll"
            ),
            os.path.join(
                os.getenv("programfiles(x86)"), "Tesseract-OCR", "libtesseract-4.dll"
            ),
        ]
    elif MAC:  # MacOS
        locations += [
            # add potential environment paths here:
            # Example:
            # os.path.join(os.getenv("MACOS_ENV_NAME"), "Tesseract-OCR", "libtesseract-4.dll"),
        ]
    elif LINUX:
        locations += [
            # add potential environment paths here:
            # Example:
            # os.path.join(os.getenv("LINUX_ENV_NAME"), "Tesseract-OCR", "libtesseract-4.dll"),
        ]

    for potential in filter(lambda x: x, locations):
        if os.path.isfile(potential):
            logger.debug(f"Using tesseract at {potential}")
            return potential

    raise TesseractError(
        "Tesseract library was not found on your system. Please install it"
    )


def set_tessdata():
    if _is_pyinstaller() or True:
        base_path = HOME
        if WINDOWS:
            base_path = os.getenv("LOCALAPPDATA") or HOME
        tessdata = os.path.join(base_path, "utsushis-charm", "tessdata")
        os.environ["TESSDATA_PREFIX"] = tessdata
        os.makedirs(tessdata, exist_ok=True)

    if "TESSDATA_PREFIX" in os.environ:
        return

    path = find_tesseract()
    path = os.path.dirname(path)
    TESSDATA_PREFIX = os.path.join(path, "tessdata")
    os.environ["TESSDATA_PREFIX"] = TESSDATA_PREFIX
    logger.debug(f"Set 'TESSDATA_PREFIX' to {TESSDATA_PREFIX}")


def get_datapath():
    if "TESSDATA_PREFIX" not in os.environ:
        set_tessdata()

    return os.environ["TESSDATA_PREFIX"]


def download_language_data(lang="eng"):
    target_dir = get_datapath()
    full_name = os.path.join(target_dir, f"{lang}.traineddata")
    if os.path.isfile(full_name):
        return

    name_map = {"eng": "English"}
    pack_name = name_map[lang]

    url = (
        f"https://github.com/tesseract-ocr/tessdata_best/raw/master/{lang}.traineddata"
    )

    print(f"Downloading {pack_name} language pack to: {target_dir}")
    with tqdm(
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
        miniters=1,
        desc=f"Downloading {pack_name} pack...",
    ) as pbar:

        request.urlretrieve(
            url, filename=full_name, reporthook=_tqdm_dl_hook(pbar), data=None
        )


def process_image_with_tesseract(tesseract, image):
    whitelist = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'/-"

    height, width = image.shape[:2]
    if len(image.shape) == 2:
        depth = 1
    else:
        depth = image.shape[2]

    # Forcing obnoxious type conversion, probably some windows BS
    image = image.astype(np.uint8)

    tesseract.set_image(image.ctypes, width, height, depth)
    tesseract.set_variable("whitelist", whitelist)
    tesseract.set_resolution()
    text = tesseract.get_text()
    return text.strip()


def _tqdm_dl_hook(tqdm_instance):
    # Source: https://github.com/tqdm/tqdm/blob/master/examples/tqdm_wget.py
    # Licence: LICENSES/tqdm (MPLv2.0 and MIT)
    """Wraps tqdm instance.
    Don't forget to close() or __exit__()
    the tqdm instance once you're done with it (easiest using `with` syntax).
    Example
    -------
    >>> with tqdm(...) as t:
    ...     reporthook = my_hook(t)
    ...     urllib.urlretrieve(..., reporthook=reporthook)
    """
    last_b = [0]

    def update_to(b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] or -1,
            remains unchanged.
        """
        if tsize not in (None, -1):
            tqdm_instance.total = tsize
        displayed = tqdm_instance.update((b - last_b[0]) * bsize)
        last_b[0] = b
        return displayed

    return update_to
