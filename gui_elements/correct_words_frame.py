import tkinter as tk
import styles


class CorrectWordsFrame:
    """A frame for correct words"""
    def __init__(self, root):
        self.correct_words_frame = tk.Frame(root, **styles.MAIN_WINDOW_STYLE)
        self.correct_words = {}

    def get_frame(self):
        return self.correct_words_frame

    def add_word(self, word):
        self.correct_words[word] = tk.Label(self.correct_words_frame, text=word, **styles.NO_BACKGROUND_LABEL_STYLE)
        self.correct_words[word].pack(fill=tk.BOTH, side=tk.TOP)

    def remove_correct_words_labels(self):
        for word in self.correct_words:
            self.correct_words[word].pack_forget()
        self.correct_words.clear()
