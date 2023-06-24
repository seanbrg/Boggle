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
        self.gui.set_start_game_button_command(self.click_on_start_game())


    def click_on_letter_button(self, button_cell_location):
        def select_letter():
            self.game.add_selected_cell(button_cell_location)
            self.gui.set_selected_word(self.game.get_selected_path_word())

        return select_letter

    def click_on_submit_word(self):
        def submit_word():
            self.game.sumbit_guessed_word()
            self.gui.set_selected_word("")
            self.gui.set_score(self.game.get_score())
            self.gui.set_correct_word(self.game.get_last_correct_word())
        return submit_word

    def click_on_start_game(self):
        def start_game():
            #todo: start timer
            self.gui.show_game_frame()
        return start_game


    def play(self):
        self.gui.run_gui()


if __name__ == '__main__':
    controller = BoggleController()
    controller.play()