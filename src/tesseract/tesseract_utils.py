from time import sleep
from urllib.error import URLError
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
from ..resources import get_language_from_code, get_tesseract_location

logger = logging.getLogger(__name__)
HOME = str(Path.home())
WINDOWS = platform.system() == "Windows"
LINUX = platform.system() == "Linux"
MAC = platform.system() == "Darwin"


def _is_pyinstaller():
    return hasattr(sys, "_MEIPASS")


def _get_pyinstaller_tesseract_path():
    base_path = sys._MEIPASS
    bundled_paths = []
    if WINDOWS:
        bundled_paths += [
            os.path.join(base_path, "Tesseract-OCR", "libtesseract-5.dll"),
            os.path.join(base_path, "libtesseract-5.dll"),
            os.path.join(base_path, "Tesseract-OCR", "libtesseract-4.dll"),
            os.path.join(base_path, "libtesseract-4.dll"),
        ]
    else:
        bundled_paths += [
            os.path.join(base_path, "libtesseract.so.5"),
            os.path.join(base_path, "libtesseract.so.4"),
        ]
    return bundled_paths


def _get_config_tesseract_path():
    locations = []
    configLocation = get_tesseract_location()

    if configLocation is not None:
        locations += [configLocation]
        if WINDOWS:
            locations += [
                os.path.join(configLocation, "libtesseract-5.dll"),
                os.path.join(configLocation, "libtesseract-4.dll"),
                os.path.join(configLocation, "libtesseract.dll"),
            ]
        else:
            locations += [
                os.path.join(configLocation, "libtesseract.so.5"),
                os.path.join(configLocation, "libtesseract.so.4"),
            ]
    return locations


def does_tess_exist():
    try:
        find_tesseract(silent=False)
        return True
    except TesseractError:
        return False


def find_tesseract(silent=False):
    locations = []
    locations += _get_config_tesseract_path()

    if _is_pyinstaller():
        print("Checking for bundled tesseract")
        locations += _get_pyinstaller_tesseract_path()

    # TODO: Make this resilient to "change" (tesseract version), probably not necessary
    locations += [
        ctypes.util.find_library("libtesseract-5"),  # win32
        ctypes.util.find_library("libtesseract-4"),  # win32
        ctypes.util.find_library("libtesseract302"),  # win32 version 3.2
        ctypes.util.find_library("libtesseract"),  # others
        ctypes.util.find_library("tesseract"),  # others
    ]

    if WINDOWS:
        locations += [
            os.path.join(
                os.getenv("ProgramW6432"), "Tesseract-OCR", "libtesseract-5.dll"
            ),
            os.path.join(
                os.getenv("LOCALAPPDATA"), "Tesseract-OCR", "libtesseract-5.dll"
            ),
            os.path.join(
                os.getenv("ProgramFiles"), "Tesseract-OCR", "libtesseract-5.dll"
            ),
            os.path.join(
                os.getenv("programfiles(x86)"), "Tesseract-OCR", "libtesseract-5.dll"
            ),
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
            # The locations should be covered by the ctypes.util.find_library("tesseract") call
        ]
    elif LINUX:
        locations += [
            # add potential environment paths here:
            # Example:
            # os.path.join(os.getenv("LINUX_ENV_NAME"), "Tesseract-OCR", "libtesseract-4.dll"),
            # The locations should be covered by the ctypes.util.find_library("tesseract") call
        ]

    for potential in filter(lambda x: x, locations):
        if os.path.isfile(potential) or potential.startswith("libtesseract.so."):
            if not silent:
                print(f"Tesseract: {potential}")
            logger.debug(f"Using tesseract at {potential}")
            return potential

    logger.error("Tesseract library was not found on your system. Please install it")
    raise TesseractError(
        "Tesseract library was not found on your system. Please install it"
    )


def use_localappdata_tess():
    base_path = HOME
    if WINDOWS:
        base_path = os.getenv("LOCALAPPDATA") or HOME
    tessdata = os.path.join(base_path, "utsushis-charm", "tessdata")
    os.environ["TESSDATA_PREFIX"] = tessdata
    os.makedirs(tessdata, exist_ok=True)


def set_tessdata():
    if _is_pyinstaller():
        use_localappdata_tess()
        return

    if "TESSDATA_PREFIX" in os.environ:
        return

    use_localappdata_tess()


def get_datapath():
    if "TESSDATA_PREFIX" not in os.environ:
        set_tessdata()

    if os.environ["TESSDATA_PREFIX"] == "tessdata":
        use_localappdata_tess()

    return os.environ["TESSDATA_PREFIX"]


def download_language_data(lang="eng", _=lambda x: x, retry=False):
    if retry:
        print(_("tess-wait-5-retry"))
        sleep(5)
    target_dir = get_datapath()
    os.makedirs(target_dir, exist_ok=True)
    full_name = os.path.join(target_dir, f"{lang}.traineddata")
    if os.path.isfile(full_name) and os.stat(full_name).st_size > 0:
        print(_("tess-found-language"))
        return

    pack_name = get_language_from_code(lang)

    url = (
        f"https://raw.githubusercontent.com/tesseract-ocr/tessdata/main/{lang}.traineddata"
        # f"https://github.com/tesseract-ocr/tessdata_best/raw/master/{lang}.traineddata"
    )

    print(_("tess-download-pack").format(pack_name, target_dir))
    e = None
    try:
        Path(full_name).touch()  # "Simple" way to test if I can write there
        request.urlretrieve(url, filename=full_name, data=None)
        print(_("tess-download-done"))
    except PermissionError as e:
        print(_("tess-permission-denied"))
        if not retry:
            use_localappdata_tess()
            download_language_data(lang, _, retry=True)
    except URLError as e:
        print(_("tess-url-error"))
        if not retry:
            download_language_data(lang, _, retry=True)
    finally:
        if e and retry:
            raise TesseractError(_("tess-cannot-download"))
        if e:
            print(e)


def process_image_with_tesseract(tesseract, image):
    whitelist = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'/-()"

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
