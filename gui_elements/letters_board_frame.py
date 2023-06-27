import tkinter as tk
from gui_elements.letter_button import LetterButton


class LettersBoardFrame:
    """A frame with GameButtons for Boggle game"""

    def __init__(self, root, game_buttons):
        self.letters_frame = tk.Frame(root)
        self._configure_grid()
        self.letters_buttons = {}
        self._init_game_buttons(game_buttons)

    def get_letters_frame(self):
        return self.letters_frame

    def get_game_buttons(self):
        return self.letters_buttons

    def _configure_grid(self):
        for i in range(4):
            self.letters_frame.columnconfigure(i, weight=1, minsize=60)
            self.letters_frame.rowconfigure(i, weight=1, minsize=60)

    def _init_game_buttons(self, game_buttons):
        for button in game_buttons:
            self.letters_buttons[button] = LetterButton(self.letters_frame, game_buttons[button], button)
            self.letters_buttons[button].position_button()
