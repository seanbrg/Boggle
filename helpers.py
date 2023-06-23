from typing import List, Tuple, Iterable, Optional
from boggle_board_randomizer import randomize_board
from ex11_utils import is_valid_path

Board = List[List[str]]
Path = List[Tuple[int, int]]
Location = Tuple[int, int]

WORDS_TXT_DICT_PATH = "boggle_dict.txt"


def create_words_set(path):
    """returns a set with the words in the given file"""
    words = set()
    with open(path, "r") as file:
        for line in file.read().split("\n"):
            words.add(line)
    return words


def cells_in_board(board: Board) -> List[Tuple[int, int]]:
    """returns an ordered list of all coordinates on the board"""
    return [(y, x) for x in range(len(board[0])) for y in range(len(board))]


def is_coordinate_in_board_limits(board: Board, coordinate: Location) -> bool:
    """return True if the coordinate is in the board's limits, else False"""
    return (0 <= coordinate[0] < len(board[0])) and (0 <= coordinate[1] < len(board))


def check_if_neighbor_cells(cell1: Location, cell2: Location) -> bool:
    """return True if the cells are next or diagonal to each other"""
    return abs(cell1[0] - cell2[0]) <= 1 and abs(cell1[1] - cell2[1]) <= 1


def get_board_cells(board: Board) -> Iterable[Location]:
    """return an iterator of cells in the board"""
    for y in range(len(board)):
        for x in range(len(board[0])):
            yield y, x


def all_valid_neighbors(cell: Location, board: Board) -> Iterable[Tuple[int, int]]:
    """return a list of coordinates of all neighboring cells of a given cell
    In practice each of these neighbors would be a valid step from the cell"""
    min_x, max_x = max(0, cell[1] - 1), min(len(board[0]), cell[1] + 1)
    min_y, max_y = max(0, cell[0] - 1), min(len(board), cell[0] + 1)
    neighbor_list = [(x, y) for x in range(min_x, max_x+1) for y in range(min_y, max_y+1)]
    if cell in neighbor_list:
        neighbor_list.remove(cell)
    # return only neighbors in the board limits:
    return filter(lambda loc: is_coordinate_in_board_limits(board, loc), neighbor_list)


def is_valid_board_path(board: Board, path: Path) -> bool:
    """return True if every two coordinates are valid neighbors"""
    for i in range(len(path) - 1):
        if path[i + 1] not in all_valid_neighbors(path[i], board):
            return False
    return True


def get_word_in_path(board: Board, path: Path) -> str:
    """connect the letters in the path to a word"""
    word = ""
    for cell in path:
        word += board[cell[0]][cell[1]]
    return word


def score(path: Path):
    """return the score that would be granted for this path"""
    return len(path) ** 2


def n_length_word(n: int, cell: Location, board: Board, word: str, word_lst: Iterable[str], path, path_lst):
    """starting from a specific cell iterate over all of its possible paths.
    when a path that assembles an n-long word is found, add it to the path list"""
    # Add current cell to the word and path
    path.append(cell)
    word += board[cell[0]][cell[1]]
    # Success condition - add the path to the path list
    if len(word) == n and word in word_lst and path not in path_lst:
        path_lst.append(path.copy())
    # Iterate on one of the cell's not-yet-used neighbors
    if len(word) <= n:
        for neighbor in all_valid_neighbors(cell, board):
            if neighbor not in path:
                n_length_word(n, neighbor, board, word, word_lst, path, path_lst)
    # Remove the cell from the word and path to backtrack
    path.remove(cell)
    word = word[:-1]


def n_length_path(n: int, cell: Location, board: Board, words: Iterable[str], word, path, path_lst):
    """starting from a specific cell iterate over all of its possible paths.
    when a path is n-long and assembles a word from the dict, add it to the path list"""
    # Add current cell to the path
    path.append(cell)
    word += board[cell[0]][cell[1]]
    # Success condition - add the path to the path list
    if len(path) == n and word in words:
        path_lst.append(path.copy())
    # Iterate on one of the cell's not-yet-used neighbors
    if len(path) <= n:
        for neighbor in all_valid_neighbors(cell, board):
            if neighbor not in path:
                n_length_path(n, neighbor, board, words, path, path_lst)
    # Remove the cell from the path to backtrack
    path.remove(cell)
    word = word[:-1]


def max_score(cell: Location, board: Board, words:Iterable[str], word, path, path_dict):
    """starting from a specific cell, iterate and backtrack along all possible path,
    and save in a dictionary the highest score paths which produce valid words"""
    # Add current cell to the path and word
    path.append(cell)
    word += board[cell[0]][cell[1]]
    # Success condition - add the path and word to the dict
    if word in words:
        if word not in path_dict.keys() or score(path) > score(path_dict[word]):
            path_dict[word] = path
    # Iterate on one of the cell's not-yet-used neighbors
    for neighbor in all_valid_neighbors(cell, board):
        if neighbor not in path:
            max_score(neighbor, board, words, word, path, path_dict)
    # Remove the cell from the path and word to backtrack
    path.remove(cell)
    word = word[:-1]
