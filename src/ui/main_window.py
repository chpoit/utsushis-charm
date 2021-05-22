import tkinter as tk
from ..text_finder import TextFinder


class MainWindow(tk.Window):
    def __init__(self, text_finder:TextFinder):
        super(MainWindow, self).__init__()

        self.text_finder = text_finder
        self.input_selector = tk.Fi