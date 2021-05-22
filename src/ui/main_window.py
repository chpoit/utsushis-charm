import os
import json
import tkinter as tk
from tkinter import filedialog, INSERT
from ..frame_extraction import extract_unique_frames
from ..charm_extraction import extract_charms, save_charms
from ..charm_encoding import encode_charms
from ..Charm import Charm, CharmList
from ..arg_builder import build_args
from ..utils import print_licenses
from ..text_finder import TextFinder


class MainWindow(tk.Tk):
    def __init__(self, text_finder: TextFinder, args):
        super(MainWindow, self).__init__()

        self.text_finder = text_finder

        self.input_dir = args.input_dir
        self.frame_dir = args.frame_dir

        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.frame_dir, exist_ok=True)

        self.charm_json = args.charm_json
        self.charm_encoded = args.charm_encoded
        self.skip_charms = args.skip_charms
        self.skip_frames = args.skip_frames

        self.charms = CharmList()

        self._build_ui()

    def _build_ui(self):
        self.input_btn = tk.Button(
            self, text="Change input directory", command=self._change_input_dir)
        self.frame_btn = tk.Button(
            self, text="Change frames directory", command=self._change_frame_dir)
        self.run_btn = tk.Button(self, text="Run", command=self.run)

        self.console = tk.Text(self)

        self.input_btn.pack()
        self.frame_btn.pack()
        self.run_btn.pack()
        self.console.pack()

    def _change_input_dir(self):
        new_dir = self._request_directory()
        if new_dir:
            self.input_dir = new_dir

    def _change_frame_dir(self):
        new_dir = self._request_directory()
        if new_dir:
            self.input_dir = new_dir

    def _request_directory(self):
        return tk.filedialog.askdirectory()

    def run(self):
        if not self.skip_frames:
            extract_unique_frames(self.input_dir, self.frame_dir)

        if not self.skip_charms:
            self.charms = extract_charms(self.frame_dir)

        self.save_charms()

    def save_charms(self):
        encoded = self.charms.encode_all()
        charm_dict = self.charm.to_dict()

        with open(self.charm_json, "w") as json_file:
            json.dump(charm_dict, json_file)
        with open(self.charm_encoded, "w") as encoded_file:
            encoded_file.write(encoded)


    def write(self, *message, end = "\n", sep = " "):
        text = ""
        for item in message:
            text += "{}".format(item)
            text += sep
        text += end
        self.console.insert(INSERT, text)
        self.update()
