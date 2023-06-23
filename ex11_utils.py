from typing import List, Tuple, Iterable, Optional
from boggle_board_randomizer import randomize_board

Board = List[List[str]]
Path = List[Tuple[int, int]]
Location = [Tuple[int, int]]

WORDS_TXT_DICT_PATH = "boggle_dict.txt"


def _create_words_set(path):
    """returns a set with the words in the given file"""
    words = set()
    with open(path, "r") as file:
        for line in file.read().split("\n"):
            words.add(line)
    return words


def _cells_in_board(board: Board) -> List[Tuple[int,int]]:
    """returns an ordered list of all coordinates on the board"""
    return [(y,x) for x in range(len(board[0])) for y in range(len(board))]


def _is_coordinate_in_board_limits(board: Board, coordinate: Location) -> bool:
    """return True if the coordinate is in the board's limits, else False"""
    return (0 <= coordinate[0] < len(board[0])) and (0 <= coordinate[1] < len(board))


def _check_if_neighbor_cells(cell1: Location, cell2: Location) -> bool:
    """return True if the cells are next or diagonal to each other"""
    return abs(cell1[0] - cell2[0]) <= 1 and abs(cell1[1] - cell2[1]) <= 1


def _all_valid_neighbors(cell: Location, board: Board) -> List[Tuple[int, int]]:
    """return a list of coordinates of all neighboring cells of a given cell
    In practice each of these neighbors would be a valid step from the cell"""
    min_x, max_x = max(0, cell[1] - 1), min(len(board[0]), cell[1] + 1)
    min_y, max_y = max(0, cell[0] - 1), min(len(board), cell[0] + 1)
    neighbor_list = [(x,y) for x in range(min_x, max_x) for y in range(min_y, max_y)]
    if cell in neighbor_list:
        neighbor_list.remove(cell)
    return neighbor_list


def _is_valid_board_path(board: Board, path: Path) -> bool:
    """return True if every two coordinates are valid neighbors"""
    for i in range(len(path)-1):
        if path[i+1] not in _all_valid_neighbors(path[i], board):
            return False
    return True


def _get_word_in_path(board: Board, path: Path):
    """connect the letters in the path to a word"""
    word = ""
    for cell in path:
        word += board[cell[0]][cell[1]]
    return word


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    if _is_valid_board_path(board, path):
        word_in_path = _get_word_in_path(board, path)
        if word_in_path in words:
            return word_in_path


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    pass


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    path_lst = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            path = []
            _n_words_helper(n, (y, x), board, '', words, path, path_lst)
    for path in path_lst:
        print(is_valid_path(board, path, words))
    return path_lst


def _n_words_helper(n: int, cell: Location, board: Board, word: str, words: Iterable[str], path, path_lst):
    """starting from a specific cell iterate and backtrack over all of its possible paths
    and write down the path until the word assembled is valid and has n letters"""
    path.append(cell)
    word += board[cell[0]][cell[1]]

    if len(word) <= n:
        if len(word) == n and word in words and path not in path_lst:
            path_lst.append(path.copy())
        for neighbor in _all_valid_neighbors(cell, board):
            if neighbor not in path:
                _n_words_helper(n, neighbor, board, word, words, path, path_lst)

    word = word[:-1]  # Remove the last character from the word
    path.remove(cell)


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    pass


if __name__ == '__main__':
    words = _create_words_set(WORDS_TXT_DICT_PATH)
    board = randomize_board()
    print(board)
    print(find_length_n_words(5, board, words))