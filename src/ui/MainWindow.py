import os
import shutil
import json
import tkinter as tk
from tkinter import filedialog, END

from ..tesseract.tesseract_utils import does_tess_exist
from ..frame_extraction import extract_unique_frames
from ..charm_extraction import extract_charms, save_charms, remove_duplicates
from ..charm_encoding import encode_charms
from ..Charm import Charm, CharmList
from ..utils import print_licenses  # TODO
from ..resources import (
    get_language_from_code,
    get_resource_path,
    get_language_code,
    get_language_list,
    get_wiki_url,
    save_app_language,
    save_game_language,
    translate_lang,
    untranslate_lang,
)
from ..translator import Translator
from .PbarWrapper import PbarWrapper
from .ParseRepairWindow import ParseRepairWindow
import webbrowser


class MainWindow(tk.Tk):
    def __init__(self, _: Translator, args, skill_language_code, app_langs):
        super().__init__()
        self.wiki_url = get_wiki_url(skill_language_code)
        self.charms = CharmList()
        self.args = args
        self._unchanged_langs = app_langs
        self._skill_language_code = skill_language_code
        self.app_langs = list(map(translate_lang, app_langs))

        self.title(_("Utsushi's Charm"))
        try:
            icon = get_resource_path("ICON")
            self.iconbitmap(icon)
        except:
            pass

        self._ = _

        self.input_dir = tk.StringVar(value=args.input_dir)
        self.frame_dir = tk.StringVar(value=args.frame_dir)
        self.lang = tk.StringVar(
            value=translate_lang(get_language_from_code(skill_language_code))
        )
        self.app_lang = tk.StringVar(value=translate_lang(_.language))

        self.charm_json = args.charm_json
        self.charm_encoded = args.charm_encoded

        self.skip_frames = tk.IntVar(value=args.skip_frames)
        self.skip_charms = tk.IntVar(value=args.skip_charms)
        self.remove_black_bars = tk.IntVar(value=False)
        self.autosave = tk.IntVar(value=1)
        self.delete_frames_val = tk.IntVar()

        self._regen_paths()
        self._build_ui()

        if not does_tess_exist():
            print(_("tess-not-found"))

    def refresh(self, _: Translator = None):
        if not _:
            _ = self._
        self.destroy()
        self.__init__(_, self.args, self._skill_language_code, self._unchanged_langs)

    def _update_lang(self, language: str):
        untranslated = untranslate_lang(language)
        if untranslated == self._.language:
            return
        code = get_language_code(untranslated)
        print(language)
        print(untranslated)
        tr = Translator(code)
        save_app_language(code)
        self.refresh(tr)

    def _update_game_lang(self, language: str):
        untranslated = untranslate_lang(language)
        code = get_language_code(untranslated)
        self._skill_language_code = code
        save_game_language(code)

    def _open_wiki(self, _: Translator = None):
        if not _:
            _ = self._
        print(_("wiki-attempt"))
        webbrowser.open(self.wiki_url)

    def _copy_wiki_url(self):
        self.clipboard_clear()
        self.clipboard_append(self.wiki_url)
        self.update()

    def _build_ui(self, _: Translator = None):
        if not _:
            _ = self._

        def _runtime_opts(parent=self):
            runtime_frame = tk.Frame(parent)
            # runtime_frame = parent
            self.autosave_box = tk.Checkbutton(
                runtime_frame, text=_("autosave-files"), variable=self.autosave
            )

            self.del_frames_box = tk.Checkbutton(
                runtime_frame, text=_("delete-frames"), variable=self.delete_frames_val
            )

            self.skip_frames_box = tk.Checkbutton(
                runtime_frame, text=_("skip-frames"), variable=self.skip_frames
            )

            self.skip_charms_box = tk.Checkbutton(
                runtime_frame, text=_("skip-charms"), variable=self.skip_charms
            )

            self.remove_black_bars_box = tk.Checkbutton(
                runtime_frame,
                text=_("remove-black-bars"),
                variable=self.remove_black_bars,
                command=self._black_bar_activated,
            )

            self.autosave_box.grid(column=1, row=1, sticky="w")
            self.del_frames_box.grid(column=1, row=2, sticky="w")
            self.skip_frames_box.grid(column=1, row=3, sticky="w")
            self.remove_black_bars_box.grid(column=1, row=4, sticky="w")

            # self.skip_charms_box.grid(column=0, row=4, sticky="w") # Hidden for now
            return runtime_frame

        def _buttons(parent=self):
            button_frame = tk.Frame(parent)
            # button_frame = parent

            self.input_btn = tk.Button(
                button_frame, text=_("change-input"), command=self._change_input_dir
            )
            self.frame_btn = tk.Button(
                button_frame, text=_("change-frames"), command=self._change_frame_dir
            )
            self.save_charms_btn = tk.Button(
                button_frame, text=_("save-charms"), command=self.save_charms
            )
            self.copy_to_clip_btn = tk.Button(
                button_frame, text=_("copy-to-clipboard"), command=self.copy_to_clip
            )

            self.lang_menu = tk.OptionMenu(
                button_frame,
                self.lang,
                *map(translate_lang, get_language_list()),
                command=self._update_game_lang,
            )

            self.input_location_lbl = tk.Label(
                button_frame, textvariable=self.input_dir
            )
            self.frames_location_lbl = tk.Label(
                button_frame, textvariable=self.frame_dir
            )

            self.lang_lbl = tk.Label(button_frame, text=_("recording-language"))

            self.app_lang_menu = tk.OptionMenu(
                button_frame,
                self.app_lang,
                *self.app_langs,
                command=self._update_lang,
            )

            self.wiki_button = tk.Button(
                button_frame, text=_("wiki-button"), command=self._open_wiki
            )

            self.wiki_clipboard_button = tk.Button(
                button_frame, text=_("wiki-clipboard"), command=self._copy_wiki_url
            )

            self.app_lang_menu.grid(column=0, row=0, sticky="w")
            self.input_btn.grid(column=0, row=1, sticky="w")
            self.frame_btn.grid(column=0, row=2, sticky="w")

            self.input_location_lbl.grid(column=1, row=1, sticky="w")
            self.frames_location_lbl.grid(column=1, row=2, sticky="w")

            self.lang_lbl.grid(column=0, row=3, sticky="w")
            self.lang_menu.grid(column=1, row=3, sticky="w")

            self.save_charms_btn.grid(column=0, row=4, sticky="w")
            self.copy_to_clip_btn.grid(column=0, row=5, sticky="w")
            self.wiki_button.grid(column=0, row=6, sticky="w")
            self.wiki_clipboard_button.grid(column=0, row=7, sticky="w")

            return button_frame

        def _progress_info(parent=self):
            progress_frame = tk.Frame(parent)

            total_files = tk.Label(progress_frame, text=_("total-files"))
            files_done = tk.Label(progress_frame, text=_("files-done"))
            frames_found = tk.Label(progress_frame, text=_("frames-found"))
            unique_frames = tk.Label(progress_frame, text=_("unique-frames"))
            charms_found = tk.Label(progress_frame, text=_("charms-found"))
            unique_charms = tk.Label(progress_frame, text=_("unique-charms"))
            file_name = tk.Label(progress_frame, text=_("current-file"))
            file_progress = tk.Label(progress_frame, text=_("file-progress"))

            self.total_files_val = tk.Label(progress_frame, text="0")
            self.files_done_val = tk.Label(progress_frame, text="0")
            self.frames_found_val = tk.Label(progress_frame, text="0")
            self.unique_frames_val = tk.Label(progress_frame, text="0")
            self.charms_found_val = tk.Label(progress_frame, text="0")
            self.unique_charms_val = tk.Label(progress_frame, text="0")
            self.current_file_val = tk.Label(progress_frame, text="")
            self.file_progress_val = tk.Label(progress_frame, text="0")

            total_files.grid(column=0, row=0, sticky="w")
            files_done.grid(column=0, row=1, sticky="w")
            frames_found.grid(column=0, row=2, sticky="w")
            unique_frames.grid(column=0, row=3, sticky="w")
            charms_found.grid(column=0, row=4, sticky="w")
            unique_charms.grid(column=0, row=5, sticky="w")
            file_name.grid(column=0, row=6, sticky="w")
            file_progress.grid(column=0, row=7, sticky="w")

            self.total_files_val.grid(column=1, row=0, sticky="w")
            self.files_done_val.grid(column=1, row=1, sticky="w")
            self.frames_found_val.grid(column=1, row=2, sticky="w")
            self.unique_frames_val.grid(column=1, row=3, sticky="w")
            self.charms_found_val.grid(column=1, row=4, sticky="w")
            self.unique_charms_val.grid(column=1, row=5, sticky="w")
            self.current_file_val.grid(column=1, row=6, sticky="w")
            self.file_progress_val.grid(column=1, row=7, sticky="w")

            return progress_frame

        self.run_btn = tk.Button(self, text=_("run"), command=self.run)
        self.pbar = PbarWrapper(self, _, length=600)
        self.console = tk.Text(self)

        self.opt_f = tk.Frame(self)
        self.runtime_opts = _runtime_opts(self.opt_f)
        self.btn_frame = _buttons(self.opt_f)
        self.progress_info = _progress_info(self.opt_f)

        pad = 5
        self.btn_frame.columnconfigure(0, weight=1)
        self.btn_frame.grid(column=0, row=0, sticky="w", pady=pad, padx=pad)

        self.runtime_opts.columnconfigure(0, weight=1)
        self.runtime_opts.grid(column=1, row=0, sticky="w", pady=pad, padx=pad)

        # self.runtime_opts.columnconfigure(1)
        self.progress_info.grid(
            column=0, row=1, sticky="w", pady=pad, padx=pad, columnspan=2
        )

        self.opt_f.columnconfigure(0, weight=1)
        self.opt_f.pack(fill="both", side="top", expand=True)

        # self.progress_info.pack( side="left", expand=False)
        self.run_btn.pack()
        self.pbar.pack()
        self.console.pack()
        self._update_save_status()

    def _change_input_dir(self):
        new_dir = self._request_directory()
        if new_dir:
            self.input_dir.set(new_dir)
            self._regen_paths()

    def _change_frame_dir(self):
        new_dir = self._request_directory()
        if new_dir:
            self.frame_dir.set(new_dir)
            self._regen_paths()

    def copy_to_clip(self, _: Translator = None):
        if not _:
            _ = self._

        self.clipboard_clear()
        self.clipboard_append(self.charms.encode_all())
        self.update()
        print(_("copied-to-clipboard"))

    def _request_directory(self):
        return tk.filedialog.askdirectory()

    def _update_save_status(self):
        if len(self.charms) == 0:
            self.save_charms_btn["state"] = "disabled"
            self.copy_to_clip_btn["state"] = "disabled"
        else:
            self.save_charms_btn["state"] = "normal"
            self.copy_to_clip_btn["state"] = "normal"

    def run(self, _: Translator = None):
        self.run_btn["state"] = "disabled"
        try:
            self._reset_progress()
            if not _:
                _ = self._
            self.print_status()
            if self.delete_frames_val.get():
                self.delete_frames()

            if not self.skip_frames.get():
                print(_("step-1-name"))
                extract_unique_frames(
                    self.input_dir.get(),
                    self.frame_dir.get(),
                    self.remove_black_bars.get(),
                    _,
                    self.pbar,
                    self.progress_callback,
                )

            if not self.skip_charms.get():
                print(_("step-2-name"))
                lang_code = get_language_code(untranslate_lang(self.lang.get()))
                self.charms = extract_charms(
                    self.frame_dir.get(),
                    lang_code,
                    _,
                    self.pbar,
                    self.progress_callback,
                )

                if self.charms.has_invalids():
                    fix_window = ParseRepairWindow(self, lang_code, self._, self.charms)
                    fix_window.fix_skills()
                    self.wait_window(fix_window)
                    repaired = fix_window.get_repaired()
                    self.charms = remove_duplicates(repaired, mode="a")
                    print(_("done-repairing"))
                    self.progress_callback({"unique_charms": len(self.charms)})

            if self.autosave.get():
                self.save_charms()

            self._update_save_status()
            self.print_end()
        except Exception as e:
            raise e
        finally:
            self.run_btn["state"] = "normal"

    def progress_callback(self, data):
        for key in data:
            if key == "total_files":
                self.total_files_val["text"] = data[key]
            elif key == "current_file":
                self.files_done_val["text"] = data[key]
            elif key == "seq":
                self.frames_found_val["text"] = data[key]
            elif key == "non_seq":
                self.unique_frames_val["text"] = data[key]
            elif key == "f_name":
                self.current_file_val["text"] = data[key]
            elif key == "charm_count":
                self.charms_found_val["text"] = data[key]
            elif key == "unique_charms":
                self.unique_charms_val["text"] = data[key]
        if "frame_count" in data and "current_frame" in data:
            c, t = data["current_frame"], data["frame_count"]
            self.file_progress_val["text"] = f"{c}/{t} {c/t*100:.2f}%"
        self.update()

    def _reset_progress(self):
        self.total_files_val["text"] = "0"
        self.files_done_val["text"] = "0"
        self.frames_found_val["text"] = "0"
        self.unique_frames_val["text"] = "0"
        self.charms_found_val["text"] = "0"
        self.unique_charms_val["text"] = "0"
        self.current_file_val["text"] = ""
        self.file_progress_val["text"] = "0"

    def print_status(self, _: Translator = None):
        if not _:
            _ = self._
        print(_("input-dir"), self.input_dir.get())
        print(_("frame-dir"), self.frame_dir.get())
        print(_("autosaving"), bool(self.autosave.get()))
        print(_("skipping-frames"), bool(self.skip_frames.get()))
        print(_("deleting-frames"), bool(self.delete_frames_val.get()))

    def print_end(self, _: Translator = None):
        if not _:
            _ = self._
        print(_("done"))
        if not self.autosave.get():
            print(_("not-saved"))
        print()

    def save_charms(self, _: Translator = None):
        if not _:
            _ = self._
        encoded = self.charms.encode_all()
        charm_dict = self.charms.to_dict()

        with open(self.charm_json, "w", encoding="utf-8") as json_file:
            json.dump(charm_dict, json_file)
        with open(self.charm_encoded, "w", encoding="utf-8") as encoded_file:
            encoded_file.write(encoded)

        print(_("charms-saved").format(self.charm_json, self.charm_encoded))

    def delete_frames(self):
        path = self.frame_dir.get()
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        elif os.path.exists(path):
            os.remove(path)
        self._regen_paths()

    def _regen_paths(self):
        os.makedirs(self.input_dir.get(), exist_ok=True)
        os.makedirs(self.frame_dir.get(), exist_ok=True)

    def _black_bar_activated(self, _=None):
        if _ is None:
            _ = self._
        if self.remove_black_bars.get():
            print(_("remove-black-bars-info"))

    def write(self, *message, end="\n", sep=" "):
        text = ""
        for item in message:
            text += f"{item}"

        self.console.insert(END, text)
        self.console.see(END)
        self.update()

    def flush(self):
        pass
