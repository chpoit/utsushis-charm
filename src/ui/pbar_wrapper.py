import tkinter as tk
import tkinter.ttk as ttk
from tqdm import tqdm
from ..text_finder import TextFinder


class PbarWrapper(ttk.Progressbar):
    def __init__(self, parent, _: TextFinder, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        self._reset_pbar()

    def __call__(self, *args, **kwargs):
        self._reset_pbar()
        self.iterable = args[0]
        if hasattr(self.iterable, "__len__"):
            self.set_total(len(self.iterable))

        for key in kwargs.keys():
            if key == "desc":
                self.set_description(kwargs[key])
            elif key == "total":
                self.set_total(kwargs[key])

        return self

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._reset_pbar()
        print()

    def __iter__(self):
        if self.iterable is not None:
            for item in self.iterable:
                yield item
                self.update(1)
        else:
            raise Exception("Nothing to iterate")

    def update(self, n):
        self["value"] += n
        self.parent.update_idletasks()

    def set_total(self, n):
        self["maximum"] = n

    def set_description(self, message):
        if not self.prev == message:
            print(message)
            self.prev = message
        pass

    def _reset_pbar(self):
        self.prev = ""
        self.iterable = None
        self["value"] = 0
        self["maximum"] = 100
