import os
import tkinter as tk
from ..utils import fix_skill_name, is_skill
from ..translator import Translator
from ..charm_extraction import repair_invalid
from ..resources import (
    get_resource_path,
    get_language_code,
    get_language_list,
    get_spell_checker,
    get_all_skills,
)
from ..Charm import Charm, CharmList, InvalidCharm
from functools import reduce
import cv2
from PIL import Image, ImageTk
import logging

logger = logging.getLogger(__name__)


class ParseRepairWindow(tk.Toplevel):
    def __init__(self, parent, language, _: Translator, charms: CharmList):
        super().__init__(parent)
        self.title(_("repair-charms"))
        try:
            icon = get_resource_path("ICON")
            self.iconbitmap(icon)
        except:
            pass

        self.language = language
        self._ = _
        self.charms = charms
        self.spell = get_spell_checker(language)
        self.all_skills = get_all_skills(language)

        self.invalid_charms = list(
            filter(lambda x: type(x) == InvalidCharm, self.charms)
        )

        self.to_fix = len(self.invalid_charms)
        self.current_idx = 0
        self.charm_iter = iter(self.invalid_charms)
        self.error_iter = iter([])
        self.fixed_skills = {}

        self.parsed = tk.StringVar(value="")
        self.lvl = tk.StringVar(value="")
        self.selected = tk.StringVar(value="")
        self.selected.trace("w", self.check_valid_skill)
        self.to_fix_str = tk.StringVar(value=f"0/{self.to_fix}")

        self._build_ui()
        self.check_valid_skill()

    def _build_ui(self, _: Translator = None):
        if not _:
            _ = self._

        def _bottom_buttons(parent=self):
            frame = tk.Frame(parent)

            btn_cancel = tk.Button(
                frame, text=_("cancel-skill"), command=self.select_cancel
            )
            btn_empty = tk.Button(
                frame, text=_("empty-skill"), command=self.select_empty
            )
            self.btn_ok = tk.Button(
                frame, text=_("enter-skill"), command=self.select_skill
            )

            entry_lbl = tk.Label(frame, text=_("true-skill-name"))
            self.input_box = tk.Entry(frame, textvariable=self.selected)

            entry_lbl.grid(row=0, columnspan=3, sticky="w")
            self.input_box.grid(row=1, columnspan=3, sticky="w")
            btn_cancel.grid(row=2, column=0, sticky="w")
            btn_empty.grid(row=2, column=1, sticky="w")
            self.btn_ok.grid(row=2, column=2, sticky="w")

            self.btn_add_anyway = tk.Button(
                frame, text=_("add-as-is"), command=self.select_as_is
            )
            self.btn_add_anyway.grid(row=3, column=0, columnspan=3)
            return frame

        def _lbl(parent=self):
            frame = tk.Frame(parent)

            self.img_lbl = tk.Label(frame, text=_("skill-img"))
            self.img_value_lbl = tk.Label(frame)

            self.text_lbl = tk.Label(frame, text=_("parsed-text"))
            self.text_value_lbl = tk.Label(frame, textvariable=self.parsed)

            self.lvl_lbl = tk.Label(frame, text=_("level"))
            self.lvl_value_lbl = tk.Label(frame, textvariable=self.lvl)

            self.to_fix_lbl = tk.Label(frame, text=_("charms-to-fix"))
            self.to_fix_value_lbl = tk.Label(frame, textvariable=self.to_fix_str)

            self.img_lbl.grid(column=0, row=0, sticky="w")
            self.img_value_lbl.grid(column=1, row=0, sticky="w")

            self.text_lbl.grid(column=0, row=1, sticky="w")
            self.text_value_lbl.grid(column=1, row=1, sticky="w")

            self.lvl_lbl.grid(column=0, row=2, sticky="w")
            self.lvl_value_lbl.grid(column=1, row=2, sticky="w")

            self.to_fix_lbl.grid(column=0, row=3, sticky="w")
            self.to_fix_value_lbl.grid(column=1, row=3, sticky="w")

            return frame

        labels = _lbl()
        btn = _bottom_buttons()

        labels.pack()
        btn.pack()

    def check_valid_skill(self, *args):
        new_name = self.selected.get()
        if not is_skill(self.all_skills, new_name):
            self.btn_add_anyway["state"] = "normal"
            self.btn_ok["state"] = "disabled"
            self.unbind("<Return>")
        else:
            self.btn_add_anyway["state"] = "disabled"
            self.btn_ok["state"] = "normal"
            self.bind("<Return>", self.select_skill)

    def fix_skills(self):
        self.repaired = CharmList()
        self.try_next_charm()

    def feed_charm(self, charm):
        self.current_idx += 1
        self.current = charm
        self.fixed_skills = charm.skills
        self.error_iter = iter(charm.get_errors())
        self.feed_error(next(self.error_iter))
        self.to_fix_str.set(f"{self.current_idx}/{self.to_fix}")

    def feed_error(self, error):
        self.current_error = error
        skill_img, parsed, level, error_type = error
        if "chi" in self.language or self.language == "kor" or self.language == "jpn":
            parsed = parsed.replace(" ", "")
        b, g, r = cv2.split(skill_img)
        im = Image.fromarray(cv2.merge((r, g, b)))
        imgtk = ImageTk.PhotoImage(image=im)
        self.img_value_lbl.configure(image=imgtk)
        self.img_value_lbl.image = imgtk
        self.parsed.set(parsed)
        self.selected.set(parsed)
        self.lvl.set(level)
        self.update()

    def get_repaired(self):
        return self.repaired + list(
            filter(lambda x: type(x) != InvalidCharm, self.charms)
        )

    def select_cancel(self):
        self.select("cancel")

    def select_empty(self):
        self.select("empty")

    def select_skill(self, *args):
        self.select("skill")

    def select_as_is(self, *args):
        self.select("as-is")

    def try_next_charm(self):
        try:
            self.feed_charm(next(self.charm_iter))
        except StopIteration:
            self.destroy()

    def try_next_error(self):
        try:
            self.feed_error(next(self.error_iter))
        except StopIteration:
            self.repaired.add(self.current.repair(self.fixed_skills))
            self.try_next_charm()

    def select(self, action):
        if action == "cancel":
            logger.warning(
                f"Charm skipped and removed through cancellation: {self.current.frame_loc}"
            )
            self.try_next_charm()
            return
        elif action == "skill":
            self.fixed_skills[
                fix_skill_name(self.all_skills, self.selected.get())
            ] = self.current_error[2]
        elif action == "as-is":
            self.fixed_skills[self.selected.get()] = self.current_error[2]

        self.try_next_error()
