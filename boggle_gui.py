import tkinter as tk
from typing import Tuple

import colors
import styles
from gui_elements.letters_board_frame import LettersBoardFrame
from gui_elements.correct_words_frame import CorrectWordsFrame
from consts import *

Location = Tuple[int, int]


class BoggleGUI:
    def __init__(self, game_buttons):
        self.root = tk.Tk()
        self._config_root()
        self.__seconds = 0
        self.__correct_words = []

        # enter frame elements:
        self.__enter_frame = tk.Frame(self.root, **styles.MAIN_WINDOW_STYLE)
        self.__enter_game_label = tk.Label(self.__enter_frame, **styles.NO_BACKGROUND_LABEL_STYLE,
                                           text=ENTER_GAME_LABEL_TEXT)
        self.__start_game_button = tk.Button(self.__enter_frame, **styles.ACTION_BUTTON_STYLE,
                                             text=START_GAME_BUTTON_TEXT)

        # game over frame elements:
        self.__game_over_frame = tk.Frame(self.root, **styles.MAIN_WINDOW_STYLE)
        self.__game_over_label = tk.Label(self.__game_over_frame, **styles.NO_BACKGROUND_LABEL_STYLE,
                                          text=GAME_OVER_LABEL_TEXT)
        self.__play_again_button = tk.Button(self.__game_over_frame, **styles.ACTION_BUTTON_STYLE,
                                             text=PLAY_AGAIN_BUTTON_TEXT)
        # game frame elements:
        self.__game_frame = tk.Frame(self.root, **styles.MAIN_WINDOW_STYLE)
        self.__timer_display_label = tk.Label(self.__game_frame, **styles.LABEL_STYLE)
        self._update_timer_label()  # set the start time
        self.__selected_word_label = tk.Label(self.__game_frame, **styles.TEXT_LABEL_STYLE)
        self.__letters_frame = LettersBoardFrame(self.__game_frame, game_buttons)
        self.__game_buttons = self.__letters_frame.get_game_buttons()  # save the cells buttons in a dict:
        self.__submit_word_button = tk.Button(self.__game_frame, text=SUBMIT_WORD_BUTTON_TEXT,
                                              **styles.ACTION_BUTTON_STYLE)
        self.__clear_word_button = tk.Button(self.__game_frame, text=CLEAR_WORD_BUTTON_TEXT,
                                             **styles.ACTION_BUTTON_STYLE)
        self.__score_label = tk.Label(self.__game_frame, text=INITIAL_SCORE_LABEL_TEXT, **styles.LABEL_STYLE)
        self.__correct_words_frame = CorrectWordsFrame(self.__game_frame)

        self.show_enter_frame()

    def _config_root(self):
        self.root.geometry("900x500")
        self.root.configure(styles.MAIN_WINDOW_STYLE)
        self.root.title(WINDOW_TITLE)

    def __position_game_frame(self):
        """position game objects in grid"""
        for i in range(12):
            self.__game_frame.columnconfigure(i, weight=1)
            self.__game_frame.rowconfigure(i, weight=1)
        self.__timer_display_label.grid(row=0, column=0, sticky=tk.NSEW, columnspan=12)
        self.__selected_word_label.grid(row=1, column=4, sticky=tk.W)
        self.__letters_frame.get_letters_frame().grid(row=2, column=0, columnspan=4, rowspan=4)
        self.__clear_word_button.grid(row=2, column=4, columnspan=2)
        self.__submit_word_button.grid(row=4, column=4, columnspan=2)
        self.__correct_words_frame.get_frame().grid(row=2, column=8, columnspan=2, rowspan=5)
        self.__score_label.grid(row=8, column=4, columnspan=2, sticky=tk.EW)

    def create_new_board(self, game_buttons):
        """reset the board and buttons for a new game"""
        self.__letters_frame.get_letters_frame().grid_forget()
        self.__letters_frame = LettersBoardFrame(self.__game_frame, game_buttons)
        self.__game_buttons = self.__letters_frame.get_game_buttons()
        self.__letters_frame.get_letters_frame().grid(row=2, column=0, columnspan=4, rowspan=4)

    def set_game_time_in_seconds(self, seconds):
        self.__seconds = seconds

    def _update_timer_label(self):
        """format time for display and update the label"""
        formatted_time = f"{(self.__seconds // 60):02} : {(self.__seconds % 60):02}"  # pad with zeros if there is only one digit
        self.__timer_display_label.configure(text=formatted_time)

    def add_correct_word(self, last_correct_word):
        """add correct word to display"""
        if last_correct_word and last_correct_word not in self.__correct_words:
            self.__correct_words.append(last_correct_word)
            self.__correct_words_frame.add_word(last_correct_word)

    def set_score_label(self, score):
        self.__score_label.configure(text=f"{SCORE_TITLE} {score}")

    def set_selected_word(self, word):
        self.__selected_word_label.configure(text=word)

    def set_letter_button_command(self, cell, command):
        self.__game_buttons[cell].set_command(command)

    def set_submit_word_button_command(self, command):
        self.__submit_word_button.configure(command=command)

    def set_clear_word_button_command(self, command):
        self.__clear_word_button.configure(command=command)

    def set_start_game_button_command(self, command):
        self.__start_game_button.configure(command=command)

    def set_play_again_button_command(self, command):
        self.__play_again_button.configure(command=command)

    def _clear_state(self):
        """reset display to start a new game"""
        self.set_selected_word("")
        self.__correct_words_frame.remove_correct_words_labels()
        self.__correct_words.clear()
        self.set_score_label(0)

    def finish_game(self):
        """clear state, switch from game frame to game over frame"""
        self._clear_state()
        self.__game_frame.pack_forget()
        self.__game_over_label.pack(pady=(150, 30))
        self.__play_again_button.pack()
        self.__game_over_frame.pack()

    def start_timer(self):
        def countdown_seconds():
            self._update_timer_label()
            self.__seconds -= 1
            if self.__seconds <= 0:
                self.finish_game()

        for i in range(self.__seconds + 1):
            self.root.after(1000 * i, countdown_seconds)

    def show_enter_frame(self):
        self.__enter_game_label.pack(pady=(150, 30))
        self.__start_game_button.pack()
        self.__enter_frame.pack()

    def show_game_frame(self):
        self.__enter_frame.pack_forget()
        self.__position_game_frame()
        self.__game_frame.pack(expand=True, fill=tk.BOTH)

    def show_game_frame_after_play_again(self):
        """switch the game over frame to game frame"""
        self.__game_over_frame.pack_forget()
        self.__position_game_frame()
        self.__game_frame.pack(expand=True, fill=tk.BOTH)

    def set_button_clicked(self, cell):
        """changes the button color and state"""
        self.__game_buttons[cell].set_bg_color(colors.CLICKED_BUTTON_COLOR)
        self.__game_buttons[cell].set_state(BUTTON_DISABLED_STATE)

    def set_button_not_clicked(self, cell):
        """changes the button color and state"""
        self.__game_buttons[cell].set_bg_color(colors.BUTTONS_COLOR)
        self.__game_buttons[cell].set_state(BUTTON_NORMAL_STATE)

    def highlight_button_color(self, cell):
        """changes the button color"""
        self.__game_buttons[cell].set_bg_color(colors.HIGHLIGHTED_BUTTON_COLOR)

    def disable_game_button(self, cell):
        """disable game cell button"""
        self.__game_buttons[cell].set_state(BUTTON_DISABLED_STATE)

    def run_gui(self):
        self.root.mainloop()
