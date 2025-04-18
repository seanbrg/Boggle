from typing import Dict, Tuple, List
from boggle_board_randomizer import randomize_board
import ex11_utils
import helpers

WORDS_TXT_DICT_PATH = "boggle_dict.txt"

Location = Tuple[int, int]


class BoggleGame:
    """Manage Boggle game logic"""
    GAME_TIME_IN_SECONDS = 180

    def __init__(self):
        self.__words = helpers.create_words_set(WORDS_TXT_DICT_PATH)
        self.__board = randomize_board()
        self.__score = 0
        self.selected_path = []
        self.correct_words = []
        self.next_valid_moves = []
        self.game_buttons = self.create_game_buttons_dict()

    def create_game_buttons_dict(self) -> Dict[Location, str]:
        """return a dict with the button cell location, and it's content"""
        buttons = {}
        for cell in helpers.get_board_cells(self.__board):
            buttons[cell] = self.__board[cell[0]][cell[1]]
        return buttons

    def get_game_buttons(self) -> Dict[Location, str]:
        return self.game_buttons

    def get_selected_path_word(self) -> str:
        return helpers.get_word_in_path(self.__board, self.selected_path)

    def get_game_time(self) -> int:
        return self.GAME_TIME_IN_SECONDS

    def add_selected_cell(self, cell) -> str:
        """append a cell to the path and return the word created from the current path"""
        self.selected_path.append(cell)

    def clear_selected_path(self) -> None:
        self.selected_path.clear()

    def get_selected_path(self) -> List[Location]:
        return self.selected_path

    def submit_guessed_word(self) -> None:
        correct_word = ex11_utils.is_valid_path(self.__board, self.selected_path, self.__words)
        if correct_word and not correct_word in self.correct_words:
            self.correct_words.append(correct_word)
            self.add_score()
        self.clear_selected_path()

    def add_score(self) -> None:
        self.__score += len(self.selected_path) ** 2

    def get_score(self) -> None:
        return self.__score

    def get_last_correct_word(self) -> str:
        return self.correct_words[-1] if self.correct_words else ""

    def get_valid_next_move_cells(self) -> List[Location]:
        """return the cells that can be the next move"""
        if not self.selected_path:
            return []
        valid_moves = []
        neighbors = helpers.all_valid_neighbors(self.selected_path[-1], self.__board)
        for neighbor in neighbors:
            if neighbor not in self.selected_path:
                valid_moves.append(neighbor)
        return valid_moves

    def set_next_valid_moves(self) -> None:
        self.next_valid_moves = self.get_valid_next_move_cells()


if __name__ == '__main__':
    game = BoggleGame()
