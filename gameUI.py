import turtle
import constants
from board import Board
from leaderboard import Leaderboard
from file_manager import FileManager


def create_custom_turtle():
    """Create a custom turtle object with penup()"""
    custom_turtle = turtle.Turtle()
    custom_turtle.penup()
    return custom_turtle


class GameUI:
    """
    Class to manage the game UI

    Attributes:
    file_manager (FileManager): The file manager object
    screen (turtle.Screen): The screen object
    leaderboard (Leaderboard): The leaderboard object
    board (Board): The board object
    ui_callbacks (dict): A dictionary of UI callbacks
    player_input (str): The player's name
    moves_input (int): The number of moves the player wants
    drawing_turtle (turtle.Turtle): The turtle object for drawing
    text (turtle.Turtle): The turtle object for text
    leaderboard_text (turtle.Turtle): The turtle object for leaderboard text
    reset_button (turtle.Turtle): The turtle object for the reset button
    load_button (turtle.Turtle): The turtle object for the load button
    quit_button (turtle.Turtle): The turtle object for the quit button
    thumbnail (turtle.Turtle): The turtle object for the thumbnail
    solvable (str): The resolvability of the puzzle
    """
    def __init__(self):
        """
        Initialize the GameUI object
        """
        turtle.tracer(0)  # Turn off the animation, very important for the game to run smoothly
        self.file_manager = FileManager()
        self.screen = turtle.Screen()
        self.leaderboard = Leaderboard()
        self.board = Board()
        self.ui_callbacks = {}
        self.player_input = ""
        self.moves_input = 0
        self.drawing_turtle = None
        self.text = None
        self.leaderboard_text = None
        self.reset_button = None
        self.load_button = None
        self.quit_button = None
        self.thumbnail = None
        self.solvable = None
        self.show_splash_screen()  # The game starts with a splash screen

    def init_callback(self):
        """
        Initialize the callbacks for the game UI
        :return: None
        """
        self.board.register_move_callback('max_puzzle', self.show_max_puzzle_error)
        self.board.register_move_callback('no_puzzle', self.show_no_puzzle_error)
        self.board.register_move_callback('redraw_thumbnail', self.draw_thumbnail)

    def register_ui_callback(self, event_type, callback):
        """
        Register a UI callback
        :param event_type: “players_name” or “moves_left”
        :param callback: The callback function
        :return: None
        """
        self.ui_callbacks[event_type] = callback

    def notify_ui_callback(self, event_type):
        """
        Notify the UI callback
        :param event_type: “players_name” or “moves_left”
        :return: None
        """
        self.ui_callbacks[event_type]()

    def show_splash_screen(self):
        """
        Show the splash screen
        :return: None
        """
        self.screen.bgpic(constants.SPLASH_SCREEN_PATH)
        self.screen.ontimer(self.check_leaderboard_error, 3000)

    def check_leaderboard_error(self):
        """
        Check if there is an error with the leaderboard file
        :return: None
        """
        self.screen.bgpic("nopic")
        if self.leaderboard.file_manager.load_leaderboard_file() == {}:
            error_turtle = create_custom_turtle()
            self.screen.register_shape(constants.LEADERBOARD_ERROR_PATH)
            error_turtle.shape(constants.LEADERBOARD_ERROR_PATH)
            turtle.update()

            def hide_shape():
                error_turtle.ht()
                error_turtle.clear()
                turtle.update()
                self.startup()

            self.screen.ontimer(hide_shape, 3000)
        else:
            self.startup()

    def show_player_info(self):
        """
        Allow the player to input player information
        :return: None
        """
        self.player_input = turtle.textinput('CS5001 Puzzle Slide', 'Your Name:')
        if self.player_input == '' or self.player_input is None:
            self.player_input = 'Anonymous'
        self.notify_ui_callback('players_name')

    def show_moves_info(self):
        """
        Allow the player to input the number of moves
        :return: None
        """
        self.moves_input = turtle.numinput('CS5001 Puzzle Slide', 'Enter the number of moves you want (5-200):',
                                           50, minval=5, maxval=200)
        self.moves_input = 50 if self.moves_input is None else int(self.moves_input)
        self.notify_ui_callback('moves_left')

    def startup(self):
        """
        A sequence of functions to start the game
        :return: None
        """
        self.show_player_info()
        self.show_moves_info()
        self.set_screen()
        self.set_turtle()
        self.set_ui()
        self.set_button()
        self.draw_board()
        self.init_callback()

    def set_screen(self):
        """
        Set the screen
        :return: None
        """
        self.screen.bgcolor("white")
        self.screen.title("CS5001 Sliding Puzzle Game")
        self.screen.setup(width=constants.SCREEN_WIDTH, height=constants.SCREEN_HEIGHT)

    def set_turtle(self):
        """
        Set the turtle objects
        :return: None
        """
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
        """
        A sequence of functions to set all the UI elements
        :return: None
        """
        self.draw_board_area()
        self.draw_button_area()
        self.draw_leaderboard_area()
        self.draw_thumbnail()
        self.write_moves(0, self.moves_input)
        self.write_leaderboard()

    def set_button(self):
        """
        Set the buttons
        :return: None
        """
        self.reset_button.goto(50, -275)
        self.screen.register_shape(constants.RESET_BUTTON_PATH)
        self.reset_button.shape(constants.RESET_BUTTON_PATH)
        self.reset_button.onclick(self.board.reset)

        self.load_button.goto(150, -275)
        self.screen.register_shape(constants.LOAD_BUTTON_PATH)
        self.load_button.shape(constants.LOAD_BUTTON_PATH)
        self.load_button.onclick(self.board.load_new_puzzle)

        self.quit_button.goto(250, -275)
        self.screen.register_shape(constants.QUIT_BUTTON_PATH)
        self.quit_button.shape(constants.QUIT_BUTTON_PATH)
        self.quit_button.onclick(self.quit_game)

        turtle.update()

    def draw_board_area(self):
        """
        Draw the board area
        :return: None
        """
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
        """
        Draw the leaderboard area
        :return: None
        """
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
        """
        Draw the button area
        :return: None
        """
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
        """
        Draw the thumbnail
        :return: None
        """
        self.thumbnail.goto(280, 330)
        thumbnail_image = self.board.puzzle_config['thumbnail']
        self.screen.register_shape(thumbnail_image)
        self.thumbnail.shape(thumbnail_image)
        turtle.update()

    def draw_board(self):
        """
        Draw the entire board
        :return: None
        """
        self.board.draw_all()

    def write_moves(self, moves, moves_left):
        """
        Write the moves information
        :param moves:Number of moves made
        :param moves_left: Number of moves left
        :return: None
        """
        self.text.goto(-300, -345)
        self.text.ht()
        self.text.write(f"Current player: {self.player_input}\nPlayer's moves: {moves}\n"
                        f"Moves left: {moves_left}\nIs it solvable? {self.board.solvable}",
                        font=("Helvetica", 30, "bold"))

    def write_leaderboard(self):
        """
        Write the leaderboard information
        :return: None
        """
        self.leaderboard_text.goto(150, -185)
        self.leaderboard_text.ht()
        self.leaderboard_text.color('blue')
        self.leaderboard_text.write(self.leaderboard.leaderboard_text(), font=("Helvetica", 19, "bold"))

    def show_max_puzzle_error(self):
        """
        Show the maximum puzzle error
        :return: None
        """
        max_error_turtle = create_custom_turtle()
        max_error_turtle.goto(0, 200)
        self.screen.register_shape(constants.MAX_PUZZLE_PATH)
        max_error_turtle.shape(constants.MAX_PUZZLE_PATH)
        turtle.update()

        def hide_shape():
            max_error_turtle.ht()
            max_error_turtle.clear()
            turtle.update()

        self.screen.ontimer(hide_shape, 2000)

    def show_no_puzzle_error(self):
        """
        Show the no puzzle error
        :return: None
        """
        no_error_turtle = create_custom_turtle()
        self.screen.register_shape(constants.NO_FILE_PATH)
        no_error_turtle.shape(constants.NO_FILE_PATH)
        turtle.update()

        def hide_shape():
            no_error_turtle.ht()
            no_error_turtle.clear()
            turtle.update()

        self.screen.ontimer(hide_shape, 2000)

    def release_click(self):
        """
        Release all the clicks
        :return: None
        """
        self.board.release_click()
        self.reset_button.onclick(None)
        self.load_button.onclick(None)
        self.quit_button.onclick(None)

    def quit_game(self, x, y):
        """
        Quit the game
        :param x: x-coordinate of the click, unused in this function
        :param y: y-coordinate of the click, unused in this function
        :return: None
        """
        self.release_click()
        bye_turtle = create_custom_turtle()
        self.screen.register_shape(constants.QUIT_MSG_PATH)
        bye_turtle.shape(constants.QUIT_MSG_PATH)
        turtle.update()
        self.screen.ontimer(self.show_credit, 3000)

    def win_game(self, x, y):
        """
        Win the game
        :param x: x-coordinate of the click, unused in this function
        :param y: y-coordinate of the click, unused in this function
        :return: None
        """
        self.release_click()
        win_turtle = create_custom_turtle()
        self.screen.register_shape(constants.WIN_MSG_PATH)
        win_turtle.shape(constants.WIN_MSG_PATH)
        turtle.update()
        self.screen.ontimer(self.show_credit, 3000)

    def lose_game(self, x, y):
        """
        Lose the game
        :param x: x-coordinate of the click, unused in this function
        :param y: y-coordinate of the click, unused in this function
        :return: None
        """
        self.release_click()
        lose_turtle = create_custom_turtle()
        self.screen.register_shape(constants.LOSE_MSG_PATH)
        lose_turtle.shape(constants.LOSE_MSG_PATH)
        turtle.update()
        self.screen.ontimer(self.show_credit, 3000)

    def show_credit(self):
        """
        Show the credits
        :return: None
        """
        credit_turtle = create_custom_turtle()
        self.screen.register_shape(constants.CREDITS_PATH)
        credit_turtle.shape(constants.CREDITS_PATH)
        turtle.update()
        self.screen.ontimer(turtle.bye, 3000)

    def mainloop(self):
        """mainloop for the game"""
        turtle.mainloop()


if __name__ == "__main__":
    game_ui = GameUI()
    game_ui.mainloop()
