import tkinter as tk
import styles


class LetterButton:
    """Letter button for Boggle game"""

    def __init__(self, parent_frame, content, position):
        self.content = content
        self.button = tk.Button(parent_frame, text=content, **styles.LETTER_BUTTON_STYLE)
        self.position = position

    def position_button(self):
        self.button.grid(row=self.position[0], column=self.position[1], sticky=tk.NSEW)

    def get_button(self):
        return self.button

    def set_command(self, command) -> None:
        self.button.configure(command=command)

    def set_bg_color(self, color):
        self.button.configure(bg=color)

    def set_state(self, state):
        self.button.configure(state=state)
