from enum import Enum
import tkinter as tk
from ..translator import Translator
from ..resources import get_resource_path
from ..updater.SimpleSemVer import SimpleSemVer


class UpdateType(Enum):
    App = 0
    Skills = 1
    AppLanguage = 2
    SkillCorrections = 3


class UpdateAction(Enum):
    Nothing = 0
    Update = 1
    Ignore = 2


class AskUpdate(tk.Toplevel):
    def __init__(
        self,
        parent,
        _: Translator,
        update_type: UpdateType,
        local: SimpleSemVer,
        remote: SimpleSemVer,
        show_ignore=False,
        patch_notes=None,
    ):
        super().__init__(parent)
        self._ = _

        self.title(_("new-version"))
        try:
            icon = get_resource_path("ICON")
            self.iconbitmap(icon)
        except:
            pass

        self.answer = False
        self.message = self.build_message(update_type, local, remote, self._)
        self.lang_lbl = tk.Label(self, text=self.message)
        self.yes_btn = tk.Button(self, text=_("yes"), command=self.yes)
        self.no_btn = tk.Button(self, text=_("no"), command=self.no)

        row = 1 if patch_notes is None else 2

        self.lang_lbl.grid(row=0, columnspan=2)
        self.yes_btn.grid(row=row, column=0, sticky="e")
        self.no_btn.grid(row=row, column=1, sticky="w")

        if show_ignore:
            self.ignore_btn = tk.Button(self, text=_("upd-ignore"), command=self.ignore)
            self.ignore_btn.grid(row=row + 1, column=0, columnspan=2)

        if patch_notes is not None:
            self.update_label = tk.Label(self, text=patch_notes)
            self.update_label.grid(row=1, columnspan=2, sticky="w")

    def build_message(self, update_type, local, remote, _):
        return _(
            {
                UpdateType.App: "new-app-update",
                UpdateType.Skills: "new-skill-update",
                UpdateType.AppLanguage: "new-app-language-update",
                UpdateType.SkillCorrections: "new-skill-correction-update",
            }[update_type]
        ).format(local, remote)

    def yes(self):
        self.answer = UpdateAction.Update
        self.destroy()

    def no(self):
        self.answer = UpdateAction.Nothing
        self.destroy()

    def ignore(self):
        self.answer = UpdateAction.Ignore
        self.destroy()
