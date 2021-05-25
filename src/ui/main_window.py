import os
import shutil
import json
import tkinter as tk
from tkinter import filedialog, END
from ..frame_extraction import extract_unique_frames
from ..charm_extraction import extract_charms, save_charms
from ..charm_encoding import encode_charms
from ..Charm import Charm, CharmList
from ..arg_builder import build_args
from ..utils import print_licenses
from ..text_finder import TextFinder
from .pbar_wrapper import PbarWrapper


class MainWindow(tk.Tk):
    def __init__(self, text_finder: TextFinder, args):
        super().__init__()
        self.charms = CharmList()

        self.text_finder = text_finder

        self.input_dir = args.input_dir
        self.frame_dir = args.frame_dir

        self.charm_json = args.charm_json
        self.charm_encoded = args.charm_encoded

        self.skip_charms = tk.IntVar(value=args.skip_charms)
        self.skip_frames = tk.IntVar(value=args.skip_frames)
        self.autosave = tk.IntVar(value=1)
        self.delete_frames_val = tk.IntVar()

        self._regen_paths()
        self._build_ui()

    def _build_ui(self, _: TextFinder = None):
        if not _:
            _ = self.text_finder

        def _runtime_opts():
            runtime_frame = tk.Frame(self)
            self.autosave_box = tk.Checkbutton(runtime_frame, text=_(
                "autosave-files"), variable=self.autosave)

            self.del_frames_box = tk.Checkbutton(runtime_frame, text=_(
                "delete-frames"), variable=self.delete_frames_val)

            self.skip_frames_box = tk.Checkbutton(runtime_frame, text=_(
                "skip-frames"), variable=self.delete_frames_val)

            self.skip_charms_box = tk.Checkbutton(runtime_frame, text=_(
                "skip-charms"), variable=self.delete_frames_val)

            self.autosave_box.pack()
            self.del_frames_box.pack()
            self.skip_frames_box.pack()
            # self.skip_charms_box.pack() # Hidden for now
            return runtime_frame

        self.input_btn = tk.Button(
            self, text=_("change-input"), command=self._change_input_dir)
        self.frame_btn = tk.Button(
            self, text=_("change-frames"), command=self._change_frame_dir)
        self.run_btn = tk.Button(self, text=_("Run"), command=self.run)

        self.pbar = PbarWrapper(self, _, length =400) 
        self.console = tk.Text(self)

        self.input_btn.pack()
        self.frame_btn.pack()
        self.run_btn.pack()

        self.runtime_opts = _runtime_opts()
        self.runtime_opts.pack()
        self.pbar.pack()
        self.console.pack()

    def _change_input_dir(self):
        new_dir = self._request_directory()
        if new_dir:
            self.input_dir = new_dir
            self._regen_paths()

    def _change_frame_dir(self):
        new_dir = self._request_directory()
        if new_dir:
            self.frames_dir = new_dir
            self._regen_paths()

    def _request_directory(self):
        return tk.filedialog.askdirectory()

    def run(self):
        self.print_status()
        if self.delete_frames_val.get():
            self.delete_frames()

        if not self.skip_frames.get():
            extract_unique_frames(self.input_dir, self.frame_dir, self.pbar)

        if not self.skip_charms.get():
            self.charms = extract_charms(self.frame_dir)

        if self.autosave.get():
            self.save_charms()

    def print_status(self, _: TextFinder = None):
        if not _:
            _ = self.text_finder
        print(_("input-dir"), self.input_dir)
        print(_("frame-dir"), self.frame_dir)
        print(_("autosaving"), bool(self.autosave.get()))
        print(_("skipping-frames"), bool(self.skip_frames.get()))
        print(_("deleting-frames"), bool(self.delete_frames_val.get()))

    def save_charms(self):
        encoded = self.charms.encode_all()
        charm_dict = self.charm.to_dict()

        with open(self.charm_json, "w") as json_file:
            json.dump(charm_dict, json_file)
        with open(self.charm_encoded, "w") as encoded_file:
            encoded_file.write(encoded)

    def delete_frames(self):
        path = self.frame_dir
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        elif os.path.exists(path):
            os.remove(path)
        self._regen_paths()

    def _regen_paths(self):
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.frame_dir, exist_ok=True)

    def write(self, *message, end="\n", sep=" "):
        text = ""
        for item in message:
            text += f"{item}"

        self.console.insert(END, text)
        self.console.see(END)
        self.update()
