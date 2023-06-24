import tkinter as tk
from gui_elements.letters_board_frame import LettersBoardFrame
from gui_elements.action_button import ActionButton
from gui_elements.score_label import ScoreLabel
from typing import Tuple, Dict, Callable

import styles
Location = Tuple[int, int]

WINDOW_TITLE = "Boggle"
SUBMIT_WORD_TEXT = "Submit"

class BoggleGUI:
    def __init__(self, game_buttons):
        self.root = tk.Tk()
        self._config_root()
        self.__letters_frame = LettersBoardFrame(self.root, game_buttons)
        self.__submit_word_button = ActionButton(self.root, SUBMIT_WORD_TEXT)
        self.selected_word_label = tk.Label(self.root, **styles.LABLE_STYLE)
        # self.score_label = tk.Label(self.root, text= "0")
        self.score_label = ScoreLabel(self.root)
        self.__game_buttons = self.__letters_frame.get_game_buttons()
        self._position_frames()


    def set_score(self, score):
        self.score_label.set_label(score)

    def _config_root(self):
        self.root.geometry("600x600")
        self.root.configure(styles.MAIN_WINDOW_STYLE)
        self.root.title(WINDOW_TITLE)

    def _position_frames(self):
        self.selected_word_label.pack(side=tk.TOP, fill=tk.X)
        self.__letters_frame.get_letters_frame().pack(side=tk.LEFT, expand=True)
        self.__submit_word_button.get_button().pack(side=tk.RIGHT, expand=True)
        self.score_label.get_label().pack(side=tk.BOTTOM)
        # self.score_label.pack(side=tk.BOTTOM)

    def set_selected_word(self, word):
        self.selected_word_label.configure(text=word)

    def get_game_letters_buttons(self):
        return self.__game_buttons

    def get_submit_word_button(self):
        return self.__submit_word_button

    def run_gui(self):
        self.root.mainloop()

