import tkinter as tk
from typing import Callable
import styles

class ActionButton:
    def __init__(self, parent_frame, content):
        self.content = content
        self.button = tk.Button(parent_frame, text=content, width=20, height=2)

    def get_button(self):
        return self.button

    def set_command(self, command: Callable[[], None]) -> None:
        self.button.configure(command=command)