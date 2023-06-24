import colors
from boggle_gui import BoggleGUI
from boggle_game import BoggleGame



class BoggleController:
    def __init__(self):
        self.game = BoggleGame()
        self.gui = BoggleGUI(self.game.get_game_buttons())
        self.set_buttons_commands()

    def set_buttons_commands(self):
        letters_buttons = self.gui.get_game_letters_buttons()
        for button in letters_buttons:
            letters_buttons[button].set_command(self.click_on_letter_button(button))

        self.gui.set_submit_word_button_command(self.click_on_submit_word())
        self.gui.set_clear_word_button_command(self.click_on_clear_word())
        self.gui.set_start_game_button_command(self.click_on_start_game())
        self.gui.set_play_again_button_command(self.click_on_play_again())


    def restart_game(self):
        self.game = BoggleGame()
        self.set_buttons_commands()

    def highlight_valid_next_moves(self, valid_moves):
        for button in self.game.get_game_buttons():
            if button not in valid_moves:
                self.gui.disable_button(button)
            else:
                self.gui.highlight_button_color(button)


    def click_on_letter_button(self, button_cell_location):
        def select_letter():
            self.reset_buttons_state()
            self.game.add_selected_cell(button_cell_location)
            self.gui.set_selected_word(self.game.get_selected_path_word())
            self.gui.set_button_clicked(button_cell_location)
            print(self.game.get_valid_next_move_cells())
            self.highlight_valid_next_moves(self.game.get_valid_next_move_cells())
        return select_letter

    def reset_buttons_state(self):
        selected_buttons = self.game.get_selected_path()
        for button in self.game.get_game_buttons():
            if button in selected_buttons:
                self.gui.set_button_clicked(button)
            else:
                self.gui.set_button_not_clicked(button)


    def click_on_submit_word(self):
        def submit_word():
            self.game.sumbit_guessed_word()
            self.gui.set_selected_word("")
            self.reset_buttons_state()
            self.gui.set_score(self.game.get_score())
            self.gui.set_correct_word(self.game.get_last_correct_word())
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
            self.gui.set_game_time_in_seconds(self.game.get_game_time())
            self.gui.start_timer()
        return start_game


    def click_on_play_again(self):
        def play_again():
            self.restart_game()
            self.reset_buttons_state()
            self.gui.show_game_frame_play_again()
            self.gui.create_new_board(self.game.get_game_buttons())
            self.gui.set_game_time_in_seconds(self.game.get_game_time())
            self.gui.start_timer()
        return play_again


    def play(self):
        self.gui.run_gui()


if __name__ == '__main__':
    controller = BoggleController()
    controller.play()