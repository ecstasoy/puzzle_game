import turtle
import constants
from board import Board
from leaderboard import Leaderboard
from file_manager import FileManager


def create_custom_turtle():
    custom_turtle = turtle.Turtle()
    custom_turtle.penup()
    return custom_turtle


class GameUI:
    def __init__(self):
        self.file_manager = FileManager()
        self.screen = turtle.Screen()
        self.leaderboard = Leaderboard()
        self.player_input = ""
        self.moves_input = 0
        turtle.tracer(0)
        self.drawing_turtle = None
        self.text = None
        self.leaderboard_text = None
        self.reset_button = None
        self.load_button = None
        self.quit_button = None
        self.thumbnail = None
        self.ui_callbacks = {}
        self.solvable = None
        self.show_splash_screen()
        self.board = Board()
        self.init_callback()

    def init_callback(self):
        self.board.register_move_callback('max_puzzle', self.show_max_puzzle_error)
        self.board.register_move_callback('no_puzzle', self.show_no_puzzle_error)

    def register_ui_callback(self, event_type, callback):
        self.ui_callbacks[event_type] = callback

    def notify_ui_callback(self, event_type):
        self.ui_callbacks[event_type]()

    def show_splash_screen(self):
        splash_screen_image = "Resources/splash_screen.gif"
        self.screen.bgpic(splash_screen_image)
        self.screen.ontimer(self.startup, 3000)

    def clear_splash_screen(self):
        self.screen.bgpic("nopic")

    def show_player_info(self):
        self.player_input = turtle.textinput('CS5001 Puzzle Slide', 'Your Name:')
        if self.player_input == '':
            self.player_input = 'Anonymous'
        self.notify_ui_callback('players_name')

    def show_moves_info(self):
        self.moves_input = int(turtle.numinput('CS5001 Puzzle Slide', 'Enter the number of moves you want (5-200):',
                                               50, minval=5, maxval=200))
        self.notify_ui_callback('moves_left')

    def startup(self):
        self.clear_splash_screen()
        self.show_player_info()
        self.show_moves_info()
        self.set_screen()
        self.set_turtle()
        self.set_ui()
        self.draw_board()
        self.set_button()

    def set_screen(self):
        self.screen.bgcolor("white")
        self.screen.title("CS5001 Sliding Puzzle Game")
        self.screen.setup(width=constants.SCREEN_WIDTH, height=constants.SCREEN_HEIGHT)

    def set_turtle(self):
        self.drawing_turtle = create_custom_turtle()
        self.drawing_turtle.hideturtle()
        self.drawing_turtle.pensize(5)
        self.text = create_custom_turtle()
        self.leaderboard_text = create_custom_turtle()
        self.reset_button = create_custom_turtle()
        self.load_button = create_custom_turtle()
        self.quit_button = create_custom_turtle()
        self.thumbnail = create_custom_turtle()

    def set_ui(self):
        self.draw_board_area()
        self.draw_button_area()
        self.draw_leaderboard_area()
        self.draw_thumbnail()
        self.write_moves(0, self.moves_input)
        self.show_leaderboard_error()
        self.write_leaderboard()

    def set_button(self):
        self.reset_button.goto(50, -275)
        reset_button_image = "Resources/resetbutton.gif"
        self.screen.register_shape(reset_button_image)
        self.reset_button.shape(reset_button_image)
        self.reset_button.onclick(self.board.reset)

        self.load_button.goto(150, -275)
        load_button_image = "Resources/loadbutton.gif"
        self.screen.register_shape(load_button_image)
        self.load_button.shape(load_button_image)
        self.load_button.onclick(self.board.load_new_puzzle)

        self.quit_button.goto(250, -275)
        quit_button_image = "Resources/quitbutton.gif"
        self.screen.register_shape(quit_button_image)
        self.quit_button.shape(quit_button_image)
        self.quit_button.onclick(self.quit_game)

        turtle.update()

    def draw_board_area(self):
        self.drawing_turtle.penup()
        self.drawing_turtle.goto(-320, 350)
        self.drawing_turtle.pendown()
        for _ in range(4):
            if _ % 2 == 0:
                self.drawing_turtle.forward(450)
                self.drawing_turtle.right(90)
            else:
                self.drawing_turtle.forward(500)
                self.drawing_turtle.right(90)

    def draw_leaderboard_area(self):
        self.drawing_turtle.color('blue')
        self.drawing_turtle.penup()
        self.drawing_turtle.goto(140, 350)
        self.drawing_turtle.pendown()
        for _ in range(4):
            if _ % 2 == 0:
                self.drawing_turtle.forward(170)
                self.drawing_turtle.right(90)
            else:
                self.drawing_turtle.forward(500)
                self.drawing_turtle.right(90)
        turtle.update()

    def draw_button_area(self):
        self.drawing_turtle.penup()
        self.drawing_turtle.goto(-320, -200)
        self.drawing_turtle.pendown()
        for _ in range(4):
            if _ % 2 == 0:
                self.drawing_turtle.forward(630)
                self.drawing_turtle.right(90)
            else:
                self.drawing_turtle.forward(150)
                self.drawing_turtle.right(90)

    def draw_thumbnail(self):
        self.thumbnail.goto(280, 330)
        thumbnail_image = self.board.puzzle_config['thumbnail']
        self.screen.register_shape(thumbnail_image)
        self.thumbnail.shape(thumbnail_image)
        turtle.update()

    def draw_board(self):
        self.board.draw()

    def write_moves(self, moves, moves_left):
        self.text.goto(-300, -345)
        self.text.ht()
        self.text.write(f"Current player: {self.player_input}\nPlayer's moves: {moves}\n"
                        f"Moves left: {moves_left}\nIs it solvable? {self.board.solvable}"
                        , font=("Helvetica", 30, "bold"))

    def write_leaderboard(self):
        self.leaderboard_text.goto(150, -185)
        self.leaderboard_text.ht()
        self.leaderboard_text.color('blue')
        self.leaderboard_text.write(self.leaderboard.leaderboard_text(), font=("Helvetica", 19, "bold"))

    def show_leaderboard_error(self):
        if self.leaderboard.file_manager.load_leaderboard_file() == {}:
            error_turtle = turtle.Turtle()
            error_turtle.penup()
            error_turtle.goto(225, 180)
            error_turtle.pendown()
            error_image = 'Resources/leaderboard_error.gif'
            self.screen.register_shape(error_image)
            error_turtle.shape(error_image)
            turtle.update()

            def hide_shape():
                error_turtle.ht()
                error_turtle.clear()

            self.screen.ontimer(hide_shape, 3000)

    def show_max_puzzle_error(self):
        max_error_turtle = turtle.Turtle()
        max_error_turtle.penup()
        max_error_turtle.goto(0, 250)
        max_error_turtle.pendown()
        max_error_image = 'Resources/file_warning.gif'
        self.screen.register_shape(max_error_image)
        max_error_turtle.shape(max_error_image)
        turtle.update()

        def hide_shape():
            max_error_turtle.ht()
            max_error_turtle.clear()
            turtle.update()

        self.screen.ontimer(hide_shape, 2000)

    def show_no_puzzle_error(self):
        no_error_turtle = turtle.Turtle()
        no_error_turtle.penup()
        no_error_turtle.goto(0, 0)
        no_error_turtle.pendown()
        no_error_image = 'Resources/file_error.gif'
        self.screen.register_shape(no_error_image)
        no_error_turtle.shape(no_error_image)
        turtle.update()

        def hide_shape():
            no_error_turtle.ht()
            no_error_turtle.clear()
            turtle.update()

        self.screen.ontimer(hide_shape, 2000)

    def release_click(self):
        self.board.release_click()
        self.reset_button.onclick(None)
        self.load_button.onclick(None)
        self.quit_button.onclick(None)

    def quit_game(self, x, y):
        self.release_click()
        bye_turtle = turtle.Turtle()
        bye_turtle.penup()
        bye_turtle.goto(0, 0)
        bye_turtle.pendown()
        exit_image = "Resources/quitmsg.gif"
        self.screen.register_shape(exit_image)
        bye_turtle.shape(exit_image)
        turtle.update()
        self.screen.ontimer(self.show_credit, 3000)

    def win_game(self, x, y):
        self.release_click()
        win_turtle = turtle.Turtle()
        win_turtle.penup()
        win_turtle.goto(0, 0)
        win_turtle.pendown()
        win_image = "Resources/winner.gif"
        self.screen.register_shape(win_image)
        win_turtle.shape(win_image)
        turtle.update()
        self.screen.ontimer(self.show_credit, 3000)

    def lose_game(self, x, y):
        self.release_click()
        lose_turtle = turtle.Turtle()
        lose_turtle.penup()
        lose_turtle.goto(0, 0)
        lose_turtle.pendown()
        lose_image = "Resources/Lose.gif"
        self.screen.register_shape(lose_image)
        lose_turtle.shape(lose_image)
        turtle.update()
        self.screen.ontimer(self.show_credit, 3000)

    def show_credit(self):
        credit_turtle = turtle.Turtle()
        credit_turtle.penup()
        credit_turtle.goto(0, 0)
        credit_turtle.pendown()
        credit_image = "Resources/credits.gif"
        self.screen.register_shape(credit_image)
        credit_turtle.shape(credit_image)
        turtle.update()
        self.screen.ontimer(turtle.bye, 3000)

    def mainloop(self):
        turtle.mainloop()


if __name__ == "__main__":
    game_ui = GameUI()
    game_ui.mainloop()
