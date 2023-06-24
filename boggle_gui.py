import tkinter as tk
from typing import Tuple

import colors
import styles
from gui_elements.letters_board_frame import LettersBoardFrame
from gui_elements.correct_words_frame import CorrectWordsFrame


Location = Tuple[int, int]

WINDOW_TITLE = "Boggle"
SUBMIT_WORD_BUTTON_TEXT = "Submit"
CLEAR_WORD_BUTTON_TEXT = "Clear"
SCORE_TITLE = "Score: "
INITIAL_SCORE_LABEL_TEXT = "0"
START_GAME_BUTTON_TEXT = "Start Game"
PLAY_AGAIN_BUTTON_TEXT = "Play Again"
BUTTON_DISABLED_STATE = "disabled"
BUTTON_NORNAL_STATE = "normal"


class BoggleGUI:
    def __init__(self, game_buttons):
        self.root = tk.Tk()
        self._config_root()
        self.seconds = 0
        # self.correct_words = {}
        self.correct_words = []

        # enter frame:
        self.enter_frame = tk.Frame(self.root, **styles.MAIN_WINDOW_STYLE)
        self.start_game_button = tk.Button(self.enter_frame, **styles.ACTION_BUTTON_STYLE, text=START_GAME_BUTTON_TEXT)
        # game over frame:
        self.game_over_frame = tk.Frame(self.root, **styles.MAIN_WINDOW_STYLE)
        self.play_again_button = tk.Button(self.game_over_frame, **styles.ACTION_BUTTON_STYLE,
                                           text=PLAY_AGAIN_BUTTON_TEXT)
        # game frame:
        self.game_frame = tk.Frame(self.root, **styles.MAIN_WINDOW_STYLE)
        self.timer_display_label = tk.Label(self.game_frame, **styles.LABEL_STYLE)
        self.middle_game_frame = tk.Frame(self.game_frame, **styles.MAIN_WINDOW_STYLE)  # to organize the game display
        self.selected_word_label = tk.Label(self.game_frame, **styles.TEXT_LABEL_STYLE)
        self.__letters_frame = LettersBoardFrame(self.middle_game_frame, game_buttons)

        # save the cells buttons in a dict:
        self.__game_buttons = self.__letters_frame.get_game_buttons()

        # action buttons frame:
        self.action_button_frame = tk.Frame(self.middle_game_frame, **styles.MAIN_WINDOW_STYLE)
        self.__submit_word_button = tk.Button(self.action_button_frame, text=SUBMIT_WORD_BUTTON_TEXT,
                                              **styles.ACTION_BUTTON_STYLE)
        self.__clear_word_button = tk.Button(self.action_button_frame, text=CLEAR_WORD_BUTTON_TEXT,
                                             **styles.ACTION_BUTTON_STYLE)

        # score frame:
        self.score_frame = tk.Frame(self.game_frame)
        self.score_label = tk.Label(self.score_frame, text=INITIAL_SCORE_LABEL_TEXT, **styles.LABEL_STYLE, width=5)

        #correct words frame:
        # self.correct_words_frame = tk.Frame(self.middle_game_frame)
        self.correct_words_frame = CorrectWordsFrame(self.middle_game_frame)
        self._position_frames()


    def set_game_time_in_seconds(self, seconds):
        self.seconds = seconds

    def update_timer_label(self):
        formatted_time = f"{(self.seconds // 60):02} : {(self.seconds % 60):02}"  # pad with zeros if there is only one digit
        self.timer_display_label.configure(text=formatted_time)

    def set_correct_word(self, last_correct_word):
        # if last_correct_word and last_correct_word not in self.correct_words:
        #     self.correct_words[last_correct_word] = tk.Label(self.correct_words_frame, text=last_correct_word,
        #                                                      **styles.CORRECT_WORDS_LABEL_STYLE)
        #     self.correct_words[last_correct_word].pack(fill=tk.BOTH)

        if last_correct_word and last_correct_word not in self.correct_words:
            self.correct_words.append(last_correct_word)
            self.correct_words_frame.add_word(last_correct_word)
        # self.correct_words[last_correct_word].pack(fill=tk.BOTH)

    def position_score_frame(self):
        """position the title and the score in a frame"""
        score_title = tk.Label(self.score_frame, text=SCORE_TITLE, **styles.LABEL_STYLE, width=10)
        score_title.pack(side=tk.LEFT)
        self.score_label.pack(side=tk.LEFT)

    def set_score(self, score):
        self.score_label.configure(text=score)

    def _config_root(self):
        self.root.geometry("1000x500")
        self.root.configure(styles.MAIN_WINDOW_STYLE)
        self.root.title(WINDOW_TITLE)


    def position_action_buttons_frame(self):
        self.__clear_word_button.pack()
        self.__submit_word_button.pack(pady=10)

    def _position_frames(self):
        self.timer_display_label.pack(expand=True, fill=tk.BOTH)
        self.selected_word_label.pack(fill=tk.X)
        self.__letters_frame.get_letters_frame().pack(side=tk.LEFT, padx=25)
        # self.__submit_word_button.pack(side=tk.LEFT, padx=25)
        # self.__clear_word_button.pack(side=tk.LEFT, padx=25)
        self.position_action_buttons_frame()
        self.action_button_frame.pack(side=tk.LEFT)
        self.correct_words_frame.get_frame().pack(side=tk.RIGHT, padx=(0, 100))
        # self.correct_words_frame.pack(side=tk.RIGHT, padx=(0, 100))
        self.middle_game_frame.pack(padx=20, pady=30, fill=tk.BOTH)
        self.score_frame.pack(side=tk.BOTTOM, pady=(0, 20))
        self.position_score_frame()
        self.start_game_button.pack(pady=200)
        self.enter_frame.pack()
        self.play_again_button.pack(pady=200)
        # self.game_frame.pack(expand=True, fill=tk.BOTH)

    def set_selected_word(self, word):
        self.selected_word_label.configure(text=word)

    def get_game_letters_buttons(self):
        return self.__game_buttons

    def set_submit_word_button_command(self, command):
        self.__submit_word_button.configure(command=command)

    def set_clear_word_button_command(self, command):
        self.__clear_word_button.configure(command=command)

    def set_start_game_button_command(self, command):
        self.start_game_button.configure(command=command)

    def set_play_again_button_command(self, command):
        self.play_again_button.configure(command=command)

    def clear_state(self):
        self.set_selected_word("")
        self.correct_words_frame.remove_correct_words_labels()
        self.correct_words.clear()
        self.set_score("0")

    def finish_game(self):
        self.clear_state()
        self.game_frame.pack_forget()

        self.game_over_frame.pack()

    def start_timer(self):
        def countdown_seconds():
            self.update_timer_label()
            self.seconds -= 1
            if self.seconds <= 0:
                self.finish_game()

        for i in range(self.seconds + 1):
            self.root.after(1000 * i, countdown_seconds)

    def show_game_frame(self):
        self.enter_frame.pack_forget()
        self.game_frame.pack(expand=True, fill=tk.BOTH)

    def show_game_frame_play_again(self):
        self.game_over_frame.pack_forget()
        self.game_frame.pack(expand=True, fill=tk.BOTH)

    def set_button_clicked(self, cell):
        """changes the button color and state"""
        self.__game_buttons[cell].set_bg_color(colors.CLICKED_BUTTON_COLOR)
        self.__game_buttons[cell].set_state(BUTTON_DISABLED_STATE)

    def set_button_not_clicked(self, cell):
        """changes the button color and state"""
        self.__game_buttons[cell].set_bg_color(colors.BUTTONS_COLOR)
        self.__game_buttons[cell].set_state(BUTTON_NORNAL_STATE)

    def highlight_button_color(self, cell):
        self.__game_buttons[cell].set_bg_color(colors.HIGHLIGHTED_BUTTON_COLOR)

    def disable_button(self, cell):
        self.__game_buttons[cell].set_state(BUTTON_DISABLED_STATE)

    def run_gui(self):
        self.root.mainloop()
