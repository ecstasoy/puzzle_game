from gameUI import GameUI


class Game:
    def __init__(self):
        self.game_ui = GameUI()
        self.player_name = None
        self.moves_left = None
        self.moves = 0
        self.game_win = False
        self.game_over = False
        self.init_callback()

    def init_callback(self):
        self.game_ui.register_ui_callback('players_name', self.update_players_name)
        self.game_ui.register_ui_callback('moves_left', self.update_moves_left)
        self.game_ui.board.register_move_callback('count_move', self.count_move)
        self.game_ui.board.register_move_callback('check_game_over', self.check_game_over)
        self.game_ui.board.register_move_callback('reset_moves', self.reset_moves)
        self.game_ui.board.register_move_callback('reset_solvable', self.reset_solvable)

    def update_moves_left(self):
        self.moves_left = self.game_ui.moves_input

    def reset_moves(self):
        self.update_moves_left()
        self.moves = 0
        self.display_moves()

    def reset_solvable(self):
        self.display_moves()

    def update_players_name(self):
        self.player_name = self.game_ui.player_input

    def count_move(self):
        self.moves += 1
        self.moves_left -= 1
        self.display_moves()

    def display_moves(self):
        self.game_ui.text.clear()
        self.game_ui.write_moves(self.moves, self.moves_left)

    def check_game_over(self):
        if self.game_ui.board.is_solved():
            self.on_game_win()
        elif self.moves_left == 0:
            self.on_game_over()

    def on_game_win(self):
        self.game_ui.leaderboard.write_leaderboard(self.player_name, self.moves)
        self.game_ui.win_game(0, 0)

    def on_game_over(self):
        self.game_ui.lose_game(0, 0)
