# taken from https://stackoverflow.com/a/21754478/6471354 and https://groups.google.com/g/tesseract-ocr/c/xvTFjYCDRQU/m/rCEwjZL3BQAJ

import numpy as np
import os
import sys
import cv2
import ctypes
import ctypes.util
import shutil
import logging
logger = logging.getLogger(__name__)


class TesseractError(Exception):
    pass


def find_tesseract():
    # TODO: Make this resilient to "change" (tesseract version), probably not necessary
    locations = [
        ctypes.util.find_library("libtesseract-4"), #win32
        ctypes.util.find_library("libtesseract302"), #win32 version 3.2
        ctypes.util.find_library("tesseract"), #others
        os.path.join(os.getenv("ProgramW6432"),
                     "Tesseract-OCR", "libtesseract-4.dll"),
        os.path.join(os.getenv('LOCALAPPDATA'),
                     "Tesseract-OCR", "libtesseract-4.dll"),
        os.path.join(os.getenv("ProgramFiles"),
                     "Tesseract-OCR", "libtesseract-4.dll"),
        os.path.join(os.getenv("programfiles(x86)"),
                     "Tesseract-OCR", "libtesseract-4.dll"),
    ]

    for potential in filter(lambda x: x, locations):
        if os.path.isfile(potential):
            logger.debug(f"Using tesseract at {potential}")
            return potential

    raise TesseractError(
        'Tesseract library was not found on your system. Please install it')


class Tesseract(object):
    _lib = None
    _api = None

    class TessBaseAPI(ctypes._Pointer):
        _type_ = type('_TessBaseAPI', (ctypes.Structure,), {})

    @classmethod
    def setup_lib(cls, lib_path=None):
        if cls._lib is not None:
            return
        if lib_path is None:
            lib_path = find_tesseract()
            if lib_path is None:
                raise TesseractError(
                    'Tesseract library was not found on your system. Please install it')
        cls._lib = lib = ctypes.CDLL(lib_path)

        # source:
        # https://github.com/tesseract-ocr/tesseract/blob/3.02.02/api/capi.h

        lib.TessBaseAPICreate.restype = cls.TessBaseAPI

        lib.TessBaseAPIDelete.restype = None  # void
        lib.TessBaseAPIDelete.argtypes = (
            cls.TessBaseAPI,)  # handle

        lib.TessBaseAPIInit3.restype = ctypes.c_int
        lib.TessBaseAPIInit3.argtypes = (
            cls.TessBaseAPI,  # handle
            ctypes.c_char_p,  # datapath
            ctypes.c_char_p)  # language

        lib.TessBaseAPISetImage.restype = None
        lib.TessBaseAPISetImage.argtypes = (
            cls.TessBaseAPI,  # handle
            ctypes.c_void_p,  # imagedata
            ctypes.c_int,    # width
            ctypes.c_int,    # height
            ctypes.c_int,    # bytes_per_pixel
            ctypes.c_int)    # bytes_per_line

        lib.TessBaseAPIGetUTF8Text.restype = ctypes.c_char_p
        lib.TessBaseAPIGetUTF8Text.argtypes = (
            cls.TessBaseAPI,)  # handle

        lib.TessBaseAPISetSourceResolution.restype = None
        lib.TessBaseAPISetSourceResolution.argtypes = (
            cls.TessBaseAPI,
            ctypes.c_int
        )

    def __init__(self, language='eng', datapath=None, lib_path=None):
        if self._lib is None:
            self.setup_lib(lib_path)
        self._api = self._lib.TessBaseAPICreate()

        # required windows nonsense
        encoded_lang = language.encode("utf-8")
        encoded_datapath = None if datapath is None else datapath.encode(
            "utf-8")

        init = self._lib.TessBaseAPIInit3(
            self._api, encoded_datapath, encoded_lang)

        if init:
            raise TesseractError(f'initialization failed ({init})')

    def __del__(self):
        if not self._lib or not self._api:
            return
        if not getattr(self, 'closed', False):
            self._lib.TessBaseAPIDelete(self._api)
            self.closed = True

    def _check_setup(self):
        if not self._lib:
            raise TesseractError('lib not configured')
        if not self._api:
            raise TesseractError('api not created')

    def set_image(self, imagedata, width, height,
                  bytes_per_pixel, bytes_per_line=None):
        self._check_setup()
        if bytes_per_line is None:
            bytes_per_line = width * bytes_per_pixel
        self._lib.TessBaseAPISetImage(self._api,
                                      imagedata, width, height,
                                      bytes_per_pixel, bytes_per_line)

    def set_resolution(self, resolution=70):
        self._lib.TessBaseAPISetSourceResolution(self._api, resolution)

    def get_text(self):
        self._check_setup()
        result = self._lib.TessBaseAPIGetUTF8Text(self._api)
        if result:
            return result.decode('utf-8')

    def get_utf8_text(self):
        self._check_setup()
        return self._lib.TessBaseAPIGetUTF8Text(self._api)

    def set_variable(self, key, val):
        self._check_setup()
        self._lib.TessBaseAPISetVariable(self._api, key, val)


def convert_to_grayscale(image_data):
    return cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)


def process_image_with_tesseract(tesseract, image):
    whitelist = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890\'/-"

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


if __name__ == '__main__':
    PACKAGE_PARENT = '..'
    SCRIPT_DIR = os.path.dirname(os.path.realpath(
        os.path.join(os.getcwd(), os.path.expanduser(__file__))))
    sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
    from src.utils import remove_non_skill_info, apply_trunc_threshold, get_skills, _trim_image_past_skill_name

    test_img = [
        "frames/frame0.png",
        "frames/frame52.png",
        "frames/frame200.png",
    ]
    test_img2 = [
        # './Untitled.png',
        # './un1.png',
        # './un2.png',
    ]
    tess = Tesseract()

    try:
        for t in test_img:
            print(t)
            img = cv2.imread(t)
            skill_only_im = remove_non_skill_info(img)

            inverted = cv2.bitwise_not(skill_only_im)
            trunc_tr = apply_trunc_threshold(inverted)

            skills = get_skills(trunc_tr, True)
            for skill_img, level in skills:
                skill_img = cv2.cvtColor(skill_img, cv2.COLOR_BGR2GRAY)
                skill_img = _trim_image_past_skill_name(skill_img)
                res = process_image_with_tesseract(tess, skill_img)
                print(res)
        pass
    except Exception as e:
        print(e)
        pass

    for t in test_img2:
        tess = Tesseract()
        img = cv2.imread(t, 0)
        res = process_image_with_tesseract(tess, img[:, :-1].astype(np.uint8))
        print("From disk:", res)
