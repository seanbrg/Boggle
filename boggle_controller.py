from typing import Tuple, List
import colors
from boggle_gui import BoggleGUI
from boggle_game import BoggleGame

Location = Tuple[int, int]


class BoggleController:
    def __init__(self):
        self.game = BoggleGame()
        self.gui = BoggleGUI(self.game.get_game_buttons())
        self.set_buttons_commands()

    def set_buttons_commands(self):
        """bind buttons to actions"""

        letters_buttons = self.gui.get_game_letters_buttons()
        for button in letters_buttons:
            letters_buttons[button].set_command(self.click_on_letter_button(button))

        self.gui.set_submit_word_button_command(self.click_on_submit_word())
        self.gui.set_clear_word_button_command(self.click_on_clear_word())
        self.gui.set_start_game_button_command(self.click_on_start_game())
        self.gui.set_play_again_button_command(self.click_on_play_again())

    def highlight_valid_next_moves(self, valid_moves: List[Location]):
        """get a list of valid moves button names (locations) and change their color on the board"""
        for button in self.game.get_game_buttons():
            if button not in valid_moves:
                self.gui.disable_game_button(button)
            else:
                self.gui.highlight_button_color(button)

    def click_on_letter_button(self, button_cell_location):
        def select_letter():
            self.reset_buttons_state()
            self.game.add_selected_cell(button_cell_location)
            self.gui.set_selected_word(self.game.get_selected_path_word())
            self.gui.set_button_clicked(button_cell_location)
            self.highlight_valid_next_moves(self.game.get_valid_next_move_cells())

        return select_letter

    def reset_buttons_state(self):
        """remove colors and disable state from buttons"""
        selected_buttons = self.game.get_selected_path()
        for button in self.game.get_game_buttons():
            if button in selected_buttons:
                self.gui.set_button_clicked(button)
            else:
                self.gui.set_button_not_clicked(button)

    def click_on_submit_word(self):
        def submit_word():
            self.game.sumbit_guessed_word()
            self.gui.set_selected_word("")  # clear the display for the next guess
            self.reset_buttons_state()
            self.gui.set_score_label(self.game.get_score())  # update the new score
            self.gui.add_correct_word(self.game.get_last_correct_word())  # update the correct words display

        return submit_word

    def click_on_clear_word(self):
        def clear_word():
            self.game.clear_selected_path()
            self.gui.set_selected_word("")
            self.reset_buttons_state()

        return clear_word

    def click_on_start_game(self):
        def start_game():
            self.gui.show_game_frame()
            self.gui.set_game_time_in_seconds(self.game.get_game_time())  # set the time by the game setting
            self.gui.start_timer()

        return start_game

    def restart_game(self):
        self.game = BoggleGame()
        self.set_buttons_commands()

    def click_on_play_again(self):
        def play_again():
            self.game = BoggleGame()
            self.gui.show_game_frame_play_again()
            self.gui.create_new_board(self.game.get_game_buttons())  # create a new board from the new game buttons
            self.set_buttons_commands()  # set command actions for the new buttons
            self.gui.set_game_time_in_seconds(self.game.get_game_time())  # reset the time
            self.gui.start_timer()

        return play_again

    def play(self):
        self.gui.run_gui()


if __name__ == '__main__':
    controller = BoggleController()
    controller.play()
