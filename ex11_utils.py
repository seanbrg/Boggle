from typing import List, Tuple, Iterable, Optional
from boggle_board_randomizer import randomize_board
import helpers

Board = List[List[str]]
Path = List[Tuple[int, int]]
Location = Tuple[int, int]

WORDS_TXT_DICT_PATH = "boggle_dict.txt"


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    """If the path is valid according to the rules and is a valid word, return the word"""
    if helpers.is_valid_board_path(board, path):
        word_in_path = helpers.get_word_in_path(board, path)
        if word_in_path in words:
            return word_in_path


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """For every cell in the board iterate a backtracking function that locates all
    n-long paths that create words from the list."""
    path_lst = []
    board_cells = helpers.get_board_cells(board)
    for cell in board_cells:
        path = []
        helpers.n_length_path(n, cell, board, words, path, path_lst)
    return path_lst


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """For every cell in the board iterate a backtracking function that locates all
    paths that create n-long words from the list."""
    path_lst = []
    board_cells = helpers.get_board_cells(board)
    for cell in board_cells:
        path = []
        helpers.n_length_word(n, cell, board, '', words, path, path_lst)
    return path_lst


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:

    path_dict = {}
    board_cells = helpers.get_board_cells(board)
    for cell in board_cells:
        path = []
        helpers.max_score(cell, board, '', words, path, path_dict)
    path_lst = [i for i in path_dict.values()]
    return path_lst


if __name__ == '__main__':
    words = helpers.create_words_set(WORDS_TXT_DICT_PATH)
    board = randomize_board()
    # TEST
    print(board)
    lst = find_length_n_paths(5, board, words)
    print(lst)
    for path in lst:
        print(is_valid_path(board, path, words))

