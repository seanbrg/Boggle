import tkinter as tk
import styles


class CorrectWordsFrame:
    """A frame for correct words"""
    def __init__(self, root):
        self.correct_words_frame = tk.Frame(root)
        self.correct_words = {}

    def get_frame(self):
        return self.correct_words_frame

    def add_word(self, word):
        self.correct_words[word] = tk.Label(self.correct_words_frame, text=word, **styles.CORRECT_WORDS_LABEL_STYLE)
        self.correct_words[word].pack(fill = tk.BOTH)

    def remove_correct_words_labels(self):
        for word in self.correct_words:
            self.correct_words[word].pack_forget()
        self.correct_words.clear()
