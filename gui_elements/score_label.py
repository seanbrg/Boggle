import tkinter as tk
from typing import Callable
import styles


class ScoreLabel:
    """Score Label for games"""
    def __init__(self, parent_frame):
        self.label = tk.Label(parent_frame, text="0")

    def get_label(self):
        return self.label
    def set_label(self, content):
        self.label.configure(text=content)