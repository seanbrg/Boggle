import tkinter as tk
from gui_elements.letters_board_frame import LettersBoardFrame
from typing import Tuple, Dict, Callable

import styles
Location = Tuple[int, int]

WINDOW_TITLE = "Boggle"
SUBMIT_WORD_TEXT = "Submit"
SCORE_TITLE = "Score: "
INITIAL_SCORE_LABEL_TEXT = "0"
START_GAME_BUTTON_TEXT= "Start Game"

class BoggleGUI:
    def __init__(self, game_buttons):
        self.root = tk.Tk()
        self._config_root()
        self.seconds=7
        # self.timer_display = tk.StringVar()
        # self.timer_display.trace("w", self.update_timer_label)
        self.game_frame = tk.Frame(self.root, **styles.MAIN_WINDOW_STYLE)
        self.timer_display_label = tk.Label(self.game_frame, **styles.LABEL_STYLE)
        self.enter_frame = tk.Frame(self.root, **styles.MAIN_WINDOW_STYLE)
        self.start_game_button = tk.Button(self.enter_frame, **styles.ACTION_BUTTON_STYLE, text=START_GAME_BUTTON_TEXT)
        self.main_frame = tk.Frame(self.game_frame, **styles.MAIN_WINDOW_STYLE)
        self.__letters_frame = LettersBoardFrame(self.main_frame, game_buttons)
        self.__submit_word_button = tk.Button(self.main_frame, text=SUBMIT_WORD_TEXT, **styles.ACTION_BUTTON_STYLE)
        self.selected_word_label = tk.Label(self.main_frame, **styles.LABEL_STYLE)
        self.score_frame = tk.Frame(self.game_frame)
        self.score_label = tk.Label(self.score_frame, text="0", **styles.LABEL_STYLE, width=5)
        self.correct_words_frame = tk.Frame(self.main_frame)
        self.score_frame_init()
        self.__game_buttons = self.__letters_frame.get_game_buttons()
        self.correct_words = {}
        self._position_frames()


    def update_timer_label(self):
        formatted_time = f"{(self.seconds// 60):02} : {(self.seconds%60):02}" # pad with zeros if there is only one digit
        self.timer_display_label.configure(text=formatted_time)

    def set_correct_word(self, last_correct_word):
        if last_correct_word and last_correct_word not in self.correct_words:
            self.correct_words[last_correct_word] = tk.Label(self.correct_words_frame, text=last_correct_word, **styles.CORRECT_WORDS_LABEL_STYLE)
            self.correct_words[last_correct_word].pack(fill=tk.BOTH)

    def score_frame_init(self):
        """position the title and the score in a frame"""
        score_title = tk.Label(self.score_frame, text=SCORE_TITLE, **styles.LABEL_STYLE, width=10)
        score_title.pack(side=tk.LEFT)
        self.score_label.pack(side=tk.LEFT)

    def set_score(self, score):
        self.score_label.configure(text=score)

    def _config_root(self):
        self.root.geometry("700x600")
        self.root.configure(styles.MAIN_WINDOW_STYLE)
        self.root.title(WINDOW_TITLE)

    def _position_frames(self):
        self.selected_word_label.pack(fill=tk.X, expand=True)
        self.__letters_frame.get_letters_frame().pack(side=tk.LEFT, padx=25)
        self.__submit_word_button.pack(side=tk.LEFT, padx=25)
        self.correct_words_frame.pack(side=tk.LEFT, padx=24)
        self.main_frame.pack(padx=20, pady=30, fill=tk.BOTH)
        self.score_frame.pack(side=tk.BOTTOM, pady=(0, 20))
        self.timer_display_label.pack()
        self.start_game_button.pack()
        self.enter_frame.pack()
        # self.game_frame.pack(expand=True, fill=tk.BOTH)

    def finish_game(self):
        self.game_frame.pack_forget()

    def start_timer(self):
        def countdown_seconds():
            self.update_timer_label()
            self.seconds -= 1
            if self.seconds < 0:
                self.finish_game()

        for i in range(self.seconds+1):
            self.root.after(1000*i, countdown_seconds)


    def show_game_frame(self):
        self.enter_frame.pack_forget()
        self.game_frame.pack(expand=True, fill=tk.BOTH)


    def set_selected_word(self, word):
        self.selected_word_label.configure(text=word)


    def get_game_letters_buttons(self):
        return self.__game_buttons

    def set_submit_word_button_command(self, command):
        self.__submit_word_button.configure(command=command)


    def set_start_game_button_command(self, command):
        self.start_game_button.configure(command=command)

    def run_gui(self):
        self.root.mainloop()

