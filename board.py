import random
import turtle
import math
import constants
from tile import Tile
from file_manager import FileManager


def tuple_to_linear_index(position, num_tiles):
    row, col = position
    return row * num_tiles + col


class Board:
    def __init__(self, puzzle_file='mario.puz'):
        self.file_manager = FileManager(puzzle_file)
        self.prev_puzzle_file = None
        self.puzzle_config = None
        self.puzzle_catalog = None
        self.num_tiles = None
        self.tile_size = None
        self.tiles = None
        self.empty_tile_position = None

        self.initialize_puzzle()

        self.solvable = 'Yes' if self.is_solvable() else 'No'
        self.on_move_callbacks = {}

    def initialize_puzzle(self):
        self.puzzle_config = self.file_manager.load_puzzle_file()
        self.puzzle_catalog = self.file_manager.load_puzzle_catalog()
        self.num_tiles = int(math.sqrt(self.puzzle_config['number']))
        if self.puzzle_config['size'] <= 90:
            self.tile_size = 90
        else:
            self.tile_size = self.puzzle_config['size'] + 5
        self.initialize_tiles()

    def initialize_tiles(self):
        self.tiles = [[None for _ in range(self.num_tiles)] for _ in range(self.num_tiles)]
        self.load_puzzle()
        self.empty_tile_position = self.find_empty_tile_position()
        self.real_scramble()

    def start_pos(self):
        start_x = constants.BOARD_OFFSET_X - (self.num_tiles / 2 * self.tile_size) + (self.tile_size / 2)
        start_y = constants.BOARD_OFFSET_Y + (self.num_tiles / 2 * self.tile_size) - (self.tile_size / 2)
        return start_x, start_y

    def draw_all(self):
        start_x, start_y = self.start_pos()
        for row in self.tiles:
            for tile in row:
                x = start_x + tile.curr_position[1] * self.tile_size
                y = start_y - tile.curr_position[0] * self.tile_size
                tile.draw(x, y)
        turtle.update()

    def load_puzzle(self):
        for i in range(1, self.num_tiles ** 2 + 1):
            row, col = divmod(i - 1, self.num_tiles)
            image_path = self.puzzle_config.get(i)
            self.tiles[row][col] = Tile(image_path, (row, col), (row, col), self.move_puzzle)

    def load_new_puzzle(self, x, y):
        text = 'Enter the name of the puzzle you want to load. Choices are:\n'
        for i in range(0, len(self.puzzle_catalog)):
            if i > 9:
                self.notify_move_callback('max_puzzle')
                break
            else:
                text += self.puzzle_catalog[i] + '\n'
        new_puzzle = turtle.textinput('Load puzzle', text)
        if new_puzzle == '' or new_puzzle is None:
            return
        elif new_puzzle not in self.puzzle_catalog:
            self.file_manager.log_error(f"Puzzle file not found - \"{new_puzzle}\" ")
            self.notify_move_callback('no_puzzle')
            return
        else:
            if self.file_manager.check_puzzle_config(new_puzzle):
                self.clear_board()
                self.file_manager.puzzle_file = new_puzzle
                self.initialize_puzzle()
                self.solvable = 'Yes' if self.is_solvable() else 'No'
                self.draw_all()
                self.notify_move_callback('redraw_thumbnail')
                self.notify_move_callback('reset_moves')
            else:
                self.notify_move_callback('no_puzzle')
                return

    def reset(self, x, y):
        self.clear_board()
        self.load_puzzle()
        self.empty_tile_position = self.find_empty_tile_position()
        self.solvable = 'Yes' if self.is_solvable() else 'No'
        self.draw_all()
        self.notify_move_callback('reset_solvable')

    def scramble(self):
        tiles_lst = [tile for row in self.tiles for tile in row]
        random.shuffle(tiles_lst)
        self.tiles = [tiles_lst[i:i + self.num_tiles] for i in range(0, len(tiles_lst), self.num_tiles)]
        for i in range(self.num_tiles):
            for j in range(self.num_tiles):
                self.tiles[i][j].curr_position = (i, j)
        self.empty_tile_position = self.find_empty_tile_position()

    def get_legal_moves(self):
        legal_moves = []
        row, col = self.empty_tile_position
        if row > 0:
            legal_moves.append((row - 1, col))
        if row < self.num_tiles - 1:
            legal_moves.append((row + 1, col))
        if col > 0:
            legal_moves.append((row, col - 1))
        if col < self.num_tiles - 1:
            legal_moves.append((row, col + 1))
        return legal_moves

    def real_scramble(self):
        moves = random.randint(5, 200)
        for _ in range(moves):
            legal_moves = random.choice(self.get_legal_moves())
            empty_row = self.empty_tile_position[0]
            empty_col = self.empty_tile_position[1]
            new_row = legal_moves[0]
            new_col = legal_moves[1]
            self.tiles[new_row][new_col], self.tiles[empty_row][empty_col] =\
                self.tiles[empty_row][empty_col], self.tiles[new_row][new_col]
            self.tiles[new_row][new_col].curr_position = (new_row, new_col)
            self.tiles[empty_row][empty_col].curr_position = self.empty_tile_position
            self.empty_tile_position = self.find_empty_tile_position()

    def move_puzzle(self, position):
        row, col = position
        empty_row, empty_col = self.empty_tile_position
        if abs(row - empty_row) + abs(col - empty_col) == 1:
            draw = self.swap(position, self.empty_tile_position)
            self.empty_tile_position = position
            start_x, start_y = self.start_pos()
            for tile in draw:
                x = start_x + tile.curr_position[1] * self.tile_size
                y = start_y - tile.curr_position[0] * self.tile_size
                tile.draw(x, y)
            turtle.update()
            self.notify_move_callback('count_move')
            self.notify_move_callback('check_game_over')

    def swap(self, prev_pos, next_pos):
        draw = []
        self.tiles[prev_pos[0]][prev_pos[1]], self.tiles[next_pos[0]][next_pos[1]] = \
            self.tiles[next_pos[0]][next_pos[1]], self.tiles[prev_pos[0]][prev_pos[1]]
        self.tiles[next_pos[0]][next_pos[1]].curr_position = next_pos
        self.tiles[prev_pos[0]][prev_pos[1]].curr_position = prev_pos
        draw.append(self.tiles[prev_pos[0]][prev_pos[1]])
        draw.append(self.tiles[next_pos[0]][next_pos[1]])
        return draw

    def register_move_callback(self, event_type, callback):
        self.on_move_callbacks[event_type] = callback

    def notify_move_callback(self, event_type):
        self.on_move_callbacks[event_type]()

    def is_solvable(self):
        inversions = self.calculate_inversions()
        if self.num_tiles % 2 != 0:
            return inversions % 2 == 0
        else:
            blank_row = self.num_tiles - self.empty_tile_position[0]
            if blank_row % 2 == 0:
                return inversions % 2 != 0
            else:
                return inversions % 2 == 0

    def calculate_inversions(self):
        inversions = 0
        tiles_lst = [tile for row in self.tiles for tile in row]
        linear_positions = [tuple_to_linear_index(tile.init_position, self.num_tiles)
                            for tile in tiles_lst if tile.init_position != (self.num_tiles - 1, self.num_tiles - 1)]
        for i in range(len(linear_positions)):
            for j in range(i + 1, len(linear_positions)):
                if linear_positions[i] > linear_positions[j]:
                    inversions += 1
        return inversions

    def is_solved(self):
        for row in self.tiles:
            for tile in row:
                if tile.curr_position == self.empty_tile_position:
                    continue
                if tile.init_position != tile.curr_position:
                    return False
        return True

    def find_empty_tile_position(self):
        for row in self.tiles:
            for tile in row:
                if tile.init_position == (self.num_tiles - 1, self.num_tiles - 1):
                    return tile.curr_position

    def clear_board(self):
        for row in self.tiles:
            for tile in row:
                tile.turtle.ht()
                tile.turtle = None

    def release_click(self):
        for row in self.tiles:
            for tile in row:
                tile.turtle.onclick(None)
