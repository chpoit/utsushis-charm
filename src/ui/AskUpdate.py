from enum import Enum
import tkinter as tk
from ..translator import Translator
from ..resources import get_resource_path
from ..updater import SimpleSemVer


class UpdateType(Enum):
    App = 0
    Skills = 1
    AppLanguage = 2
    SkillCorrections = 3


class AskUpdate(tk.Toplevel):
    def __init__(
        self,
        parent,
        _: Translator,
        update_type: UpdateType,
        local: SimpleSemVer,
        remote: SimpleSemVer,
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

        self.lang_lbl.grid(row=0, columnspan=2)
        self.yes_btn.grid(row=1, column=0, sticky="e")
        self.no_btn.grid(row=1, column=1, sticky="w")

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
        self.answer = True
        self.destroy()

    def no(self):
        self.answer = False
        self.destroy()
