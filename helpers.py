from typing import List, Tuple, Iterable

Board = List[List[str]]
Path = List[Tuple[int, int]]
Location = Tuple[int, int]


def create_words_set(path: str):
    """returns a set with the words in the given file"""
    words = set()
    with open(path, "r") as file:
        for line in file.read().split("\n"):
            words.add(line)
    return words


def create_words_dict(words_set: Iterable[str]) -> dict[int:Iterable[str]]:
    words_dict = {}
    for i in range(max_length_word(words_set) + 1):
        words_dict[i] = set()
    for word in words_set:
            words_dict[len(word)].add(word)
    return words_dict


def get_board_cells(board: Board) -> Iterable[Location]:
    """return an iterator of cells in the board"""
    for y in range(len(board)):
        for x in range(len(board[0])):
            yield y, x


def all_valid_neighbors(cell: Location, board: Board) -> Iterable[Tuple[int, int]]:
    """return a list of coordinates of all neighboring cells of a given cell
    In practice each of these neighbors would be a valid step from the cell"""
    min_x, max_x = max(0, cell[1] - 1), min(len(board[0])-1, cell[1] + 1)
    min_y, max_y = max(0, cell[0] - 1), min(len(board)-1, cell[0] + 1)
    neighbor_list = [(y, x) for x in range(min_x, max_x+1) for y in range(min_y, max_y+1)]
    if cell in neighbor_list:
        neighbor_list.remove(cell)
    return neighbor_list


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


def max_length_word(words: Iterable[str]) -> int:
    """return the length of the longest word"""
    length = 0
    for word in words:
        if length < len(word):
            length = len(word)
    return length


def score(path: Path) -> int:
    """return the score that would be granted for this path"""
    return len(path) ** 2


def check_word(target_word: str, words: dict[int:Iterable[str]]) -> bool:
    """if any word in the dict contains the target word return True"""
    for word in words[len(target_word)]:
        if word.startswith(target_word):
            return True
    return False


def n_length(type, word, n, cell, board, word_lst: Iterable[str], path, path_lst):
    """starting from a specific cell iterate over all of its possible paths.
    when a path that assembles a valid word is found, add it to the path list if path/word length is n"""
    # Add current cell to the word and path
    path.append(cell)
    word += board[cell[0]][cell[1]]
    # Determine what is being measured
    length = len(word) if type == 'word' else len(path)
    # Success condition - add the path to the path list
    if length == n and word in word_lst and path not in path_lst:
        path_lst.append(path.copy())
    # Iterate on one of the cell's not-yet-used neighbors
    if length <= n:
        for neighbor in all_valid_neighbors(cell, board):
            if neighbor not in path:
                n_length(type, word, n, neighbor, board, word_lst, path, path_lst)
    # Remove the cell from the word and path to backtrack
    path.remove(cell)
    word = word[:-1]


def max_score(cell, board, word, word_dict: dict[int:Iterable[str]], max_l, path, path_dict):
    """starting from a specific cell, iterate and backtrack along all possible path,
    and save in a dictionary the highest score paths which produce valid words"""
    # Add current cell to the path and word
    path.append(cell)
    word += board[cell[0]][cell[1]]
    # Success condition - add the path and word to the dict
    if word not in path_dict.keys() or score(path) > score(path_dict[word]):
        if word in word_dict[len(word)]:
            path_dict[word] = path.copy()
    # Iterate on one of the cell's not-yet-used neighbors
    if len(word) <= max_l and (len(word) < 4 or check_word(word, word_dict)):
        for neighbor in all_valid_neighbors(cell, board):
            if neighbor not in path:
                max_score(neighbor, board, word, word_dict, max_l, path, path_dict)
    # Remove the cell from the path and word to backtrack
    path.remove(cell)
    word = word[:-1]
