# taken from https://stackoverflow.com/a/21754478/6471354 and https://groups.google.com/g/tesseract-ocr/c/xvTFjYCDRQU/m/rCEwjZL3BQAJ

import sys
import cv2
import ctypes
import ctypes.util
from datetime import datetime
import faulthandler
faulthandler.enable()


# TODO: Make this resilient to "change" (version)
if sys.platform == 'win32':
    LIBNAME = 'libtesseract-4'
else:
    LIBNAME = 'tesseract'

class TesseractError(Exception):
    pass

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
            lib_path = ctypes.util.find_library(LIBNAME)
            if lib_path is None:
                 raise TesseractError('tesseract library not found')
        cls._lib = lib = ctypes.CDLL(lib_path)

        # source:
        # https://github.com/tesseract-ocr/tesseract/
        #         blob/3.02.02/api/capi.h

        lib.TessBaseAPICreate.restype = cls.TessBaseAPI

        lib.TessBaseAPIDelete.restype = None # void
        lib.TessBaseAPIDelete.argtypes = (
            cls.TessBaseAPI,) # handle

        lib.TessBaseAPIInit3.restype = ctypes.c_int
        lib.TessBaseAPIInit3.argtypes = (
            cls.TessBaseAPI, # handle
            ctypes.c_char_p, #datapath
            ctypes.c_char_p) # language

        lib.TessBaseAPISetImage.restype = None
        lib.TessBaseAPISetImage.argtypes = (
            cls.TessBaseAPI, # handle
            ctypes.c_void_p, # imagedata
            ctypes.c_int,    # width
            ctypes.c_int,    # height
            ctypes.c_int,    # bytes_per_pixel
            ctypes.c_int)    # bytes_per_line

        lib.TessBaseAPIGetUTF8Text.restype = ctypes.c_char_p
        lib.TessBaseAPIGetUTF8Text.argtypes = (
            cls.TessBaseAPI,) # handle

        lib.TessBaseAPISetSourceResolution.restype = None
        lib.TessBaseAPISetSourceResolution.argtypes = (
            cls.TessBaseAPI,
            ctypes.c_int
        )

    def __init__(self, language='eng', datapath=None, lib_path=None):
        if self._lib is None:
            self.setup_lib(lib_path)
        self._api = self._lib.TessBaseAPICreate()

        encoded_lang = language.encode("utf-8")
        encoded_datapath = None if datapath is None else datapath.encode("utf-8")
        init = self._lib.TessBaseAPIInit3(self._api, encoded_datapath, encoded_lang)

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
    tesseract.set_variable("whitelist", whitelist)

    height, width = image.shape[:2]
    if len(image.shape)==2:
        depth = 1
    else:
        depth = image.shape[2]

    print("Shape:", image.shape)

    tesseract.set_image(image.ctypes, width, height, depth)
    tesseract.set_resolution()
    text = tesseract.get_text()
    print(text)
    print(tesseract.get_utf8_text())
    return text.strip()



if __name__ == '__main__':
    test_img =[
        './Untitled.png',
        './un1.png',
    ]
    for t in test_img:
        # img = cv2.imread('./frames/frame0.png')
        img = cv2.imread(t)
        # height, width, depth = img.shape
        tess = Tesseract()
        res = process_image_with_tesseract(tess, img)
        print(res)
