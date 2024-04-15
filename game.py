from gameUI import GameUI


class Game:
    """
    Game class is the main class that controls the game logic.

    Attributes:
    game_ui (GameUI): The game UI object.
    player_name (str): The player's name.
    moves_left (int): The number of moves left.
    moves (int): The number of moves made.
    game_win (bool): True if the game is won, False otherwise.
    game_over (bool): True if the game is over, False otherwise.
    """
    def __init__(self):
        """Initialize the Game object."""
        self.game_ui = GameUI()
        self.player_name = None
        self.moves_left = None
        self.moves = 0
        self.game_win = False
        self.game_over = False
        self.init_callback()

    def init_callback(self):
        """
        Initialize the callback functions.
        :return: None
        """
        self.game_ui.register_ui_callback('players_name', self.update_players_name)
        self.game_ui.register_ui_callback('moves_left', self.update_moves_left)
        self.game_ui.board.register_move_callback('count_move', self.count_move)
        self.game_ui.board.register_move_callback('check_game_over', self.check_game_over)
        self.game_ui.board.register_move_callback('reset_moves', self.reset_moves)
        self.game_ui.board.register_move_callback('reset_solvable', self.reset_solvable)

    def update_moves_left(self):
        """
        Update the number of moves left.
        :return: None
        """
        self.moves_left = self.game_ui.moves_input

    def reset_moves(self):
        """
        Reset the moves made.
        :return: None
        """
        self.update_moves_left()
        self.moves = 0
        self.display_moves()

    def reset_solvable(self):
        """
        Reset the display of resolvability of the board.
        :return: None
        """
        self.display_moves()

    def update_players_name(self):
        """
        Update the player's name.
        :return: None
        """
        self.player_name = self.game_ui.player_input

    def count_move(self):
        """
        Count the moves made.
        :return: None
        """
        self.moves += 1
        self.moves_left -= 1
        self.display_moves()

    def display_moves(self):
        """
        Display the moves made and the moves left.
        :return: None
        """
        self.game_ui.text.clear()
        self.game_ui.write_moves(self.moves, self.moves_left)

    def check_game_over(self):
        """
        Check if the game is over.
        :return: None
        """
        if self.game_ui.board.is_solved():
            self.on_game_win()
        elif self.moves_left == 0:
            self.on_game_over()

    def on_game_win(self):
        """
        Callback function when the game is won.
        :return: None
        """
        self.game_ui.leaderboard.write_leaderboard(self.player_name, self.moves)
        self.game_ui.win_game(0, 0)

    def on_game_over(self):
        """
        Callback function when the game is over.
        :return: None
        """
        self.game_ui.lose_game(0, 0)
