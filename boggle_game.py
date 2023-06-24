from typing import Dict, Tuple, Callable
from boggle_board_randomizer import randomize_board
import ex11_utils
import helpers
WORDS_TXT_DICT_PATH = "boggle_dict.txt"

Location = Tuple[int, int]

class BoggleGame:
    """Manage boggle game logic"""
    def __init__(self):
        self.__board = [['A', 'L', 'N', 'WF'], ['T', 'L', 'E', 'L'], ['C', 'O', 'G', 'Y'], ['S', 'E', 'R', 'H']]
        self.__words = helpers.create_words_set(WORDS_TXT_DICT_PATH)
        # self.__board = randomize_board()
        self.__score = 0
        self.selected_path = []
        self.correct_words = []
        self.game_buttons = self.create_game_buttons_dict()



    def create_game_buttons_dict(self) -> Dict[Location, str]:
        """return a dict with the button cell location and it's content"""
        buttons = {}
        for cell in helpers.get_board_cells(self.__board):
            buttons[cell] = self.__board[cell[0]][cell[1]]
        return buttons

    def get_game_buttons(self):
        return self.game_buttons

    def get_selected_path_word(self):
        return helpers.get_word_in_path(self.__board, self.selected_path)


    def add_selected_cell(self, cell) -> str:
        """append a cell to the path and return the word created from the current path"""
        self.selected_path.append(cell)


    def reset_selection(self):
        self.selected_path = []

    def sumbit_guessed_word(self):
        correct_word = ex11_utils.is_valid_path(self.__board, self.selected_path, self.__words)
        if correct_word and not correct_word in self.correct_words:
            self.correct_words.append(correct_word)
            self.add_score()
        self.reset_selection()
        print(self.__score)

    def add_score(self):
        self.__score += len(self.selected_path)**2

    def get_score(self):
        return self.__score



if __name__ == '__main__':
    game = BoggleGame()
    buttons_dict = game.get_game_buttons()
