from typing import List, Tuple, Iterable, Optional
from boggle_board_randomizer import randomize_board
import helpers

Board = List[List[str]]
Path = List[Tuple[int, int]]
Location = Tuple[int, int]

WORDS_TXT_DICT_PATH = "boggle_dict.txt"


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    """if the path is valid according to the rules and is a valid word, return the word"""
    if helpers.is_valid_board_path(board, path):
        word_in_path = helpers.get_word_in_path(board, path)
        if word_in_path in words:
            return word_in_path


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """for every cell in the board iterate a backtracking function that locates all
    n-long paths that create words from the list."""
    path_lst = []
    board_cells = helpers.get_board_cells(board)
    for cell in board_cells:
        path = []
        helpers.n_length('path', '', n, cell, board, words, path, path_lst)
    return path_lst


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """for every cell in the board iterate a backtracking function that locates all
    paths that create n-long words from the list."""
    path_lst = []
    board_cells = helpers.get_board_cells(board)
    for cell in board_cells:
        path = []
        helpers.n_length('word', '', n, cell, board, words, path, path_lst)
    return path_lst


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    """for every cell in the board iterate a backtracking function that locates all
    paths that create valid words and record the highest scoring path for each word."""
    path_dict = {}
    words_dict = helpers.create_words_dict(words)
    board_cells = helpers.get_board_cells(board)
    max_l = list(words_dict.keys())[-1]
    for cell in board_cells:
        path = []
        helpers.max_score(cell, board, '', words_dict, max_l, path, path_dict)
    # Return the values of the dictionary - all paths found - as a list
    return list(path_dict.values())


if __name__ == '__main__':
    words = helpers.create_words_set(WORDS_TXT_DICT_PATH)
    board = randomize_board()
    # TEST
    lst = max_score_paths(board, words)
    print(lst)
    """for path in lst:
        print(is_valid_path(board, path, words))
        print(helpers.score(path))"""

