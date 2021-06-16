from enum import Enum
import tkinter as tk
from ..charm import CharmList, CharmGrade, GradedCharm
from ..resources import get_resource_path
from ..utils import set_window_icon


class RebirthWindow(tk.Toplevel):
    def __init__(self, parent, _: Translator):
        super().__init__(parent)
        self._ = _

        self.title(_("rebirth-title"))
        set_window_icon(self)

    def close(self):
        self.destroy()
