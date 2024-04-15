import random
import turtle
import math
import constants
from tile import Tile
from file_manager import FileManager


def tuple_to_linear_index(position, num_tiles):
    """
    Convert a tuple position to a linear index
    :param position: position tuple
    :param num_tiles: number of tiles per line
    :return: linear index
    """
    row, col = position
    return row * num_tiles + col


class Board:
    """
    Class that represents the board of the puzzle

    Attributes:
    file_manager (FileManager): The file manager object
    puzzle_config (dict): The configuration of the puzzle
    puzzle_catalog (list): The list of available puzzles
    num_tiles (int): The number of tiles per line in the puzzle
    tile_size (int): The (pixel) size of the tiles
    tiles (list): The list of tiles
    empty_tile_position (tuple): The position of the empty tile
    solvable (str): The resolvability of the puzzle
    on_move_callbacks (dict): The dictionary of callbacks for the moves
    """
    def __init__(self, puzzle_file='mario.puz'):
        """
        Constructor of the Board class
        :param puzzle_file: The name of the puzzle file, default is 'mario.puz'
        """
        self.file_manager = FileManager(puzzle_file)
        self.puzzle_config = None
        self.puzzle_catalog = None
        self.num_tiles = None
        self.tile_size = None
        self.tiles = None
        self.empty_tile_position = None

        self.initialize_puzzle()  # Initialize the puzzle

        self.solvable = 'Yes' if self.is_solvable() else 'No'
        self.on_move_callbacks = {}

    def register_move_callback(self, event_type, callback):
        """
        Register a callback for a click-to-move event
        :param event_type: the type of event, e.g. 'max_puzzle'
        :param callback: callback function
        :return: None
        """
        self.on_move_callbacks[event_type] = callback

    def notify_move_callback(self, event_type):
        """
        Notify the callback for a click-to-move event
        :param event_type: the type of event, e.g. 'max_puzzle'
        :return: None
        """
        self.on_move_callbacks[event_type]()

    def initialize_puzzle(self):
        """
        Initialize the puzzle configuration
        :return: None
        """
        self.puzzle_config = self.file_manager.load_puzzle_file()
        self.puzzle_catalog = self.file_manager.load_puzzle_catalog()
        self.num_tiles = int(math.sqrt(self.puzzle_config['number']))
        # Set the tile size, preventing the tiles from being too small
        if self.puzzle_config['size'] <= 90:
            self.tile_size = 90
        else:
            self.tile_size = self.puzzle_config['size'] + 5
        self.initialize_tiles()

    def initialize_tiles(self):
        """
        Initialize the tiles of the puzzle
        :return: None
        """
        self.tiles = [[None for _ in range(self.num_tiles)] for _ in range(self.num_tiles)]
        self.load_puzzle()
        self.empty_tile_position = self.find_empty_tile_position()
        self.real_scramble()  # Scramble the puzzle. Change to scramble() for non-guaranteed resolvability

    def start_pos(self):
        """
        Calculate the starting position when drawing the puzzle
        :return: a tuple of the starting position
        """
        start_x = constants.BOARD_OFFSET_X - (self.num_tiles / 2 * self.tile_size) + (self.tile_size / 2)
        start_y = constants.BOARD_OFFSET_Y + (self.num_tiles / 2 * self.tile_size) - (self.tile_size / 2)
        return start_x, start_y

    def draw_all(self):
        """
        Draw all the tiles of the puzzle
        :return: None
        """
        start_x, start_y = self.start_pos()
        for row in self.tiles:
            for tile in row:
                # Calculate the drawing position of the tile
                x = start_x + tile.curr_position[1] * self.tile_size
                y = start_y - tile.curr_position[0] * self.tile_size
                tile.draw(x, y)  # Invoke the draw method of the tile
        turtle.update()  # Update the turtle screen

    def load_puzzle(self):
        """
        Load the puzzle configuration, put tiles in the 2D list
        :return: None
        """
        for i in range(1, self.num_tiles ** 2 + 1):
            # Calculate the row and column of the tile
            row, col = divmod(i - 1, self.num_tiles)
            image_path = self.puzzle_config.get(i)
            # Create a new instance of the Tile class for each tile
            self.tiles[row][col] = Tile(image_path, (row, col), (row, col), self.move_puzzle)

    def load_new_puzzle(self, x, y):
        """
        Load a new puzzle from files and redraw the puzzle
        :param x: x-coordinate of the click, not used here
        :param y: y-coordinate of the click, not used here
        :return: None
        """
        text = 'Enter the name of the puzzle you want to load. Choices are:\n'
        for i in range(0, len(self.puzzle_catalog)):
            # Show the first 10 puzzles
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
            # Check if the new puzzle is valid
            if self.file_manager.check_puzzle_config(new_puzzle):
                self.clear_board()
                self.file_manager.puzzle_file = new_puzzle
                self.initialize_puzzle()
                self.solvable = 'Yes' if self.is_solvable() else 'No'
                self.draw_all()
                self.notify_move_callback('redraw_thumbnail')
                self.notify_move_callback('reset_moves')
            # If the new puzzle is not valid, show and log an error
            else:
                self.notify_move_callback('no_puzzle')
                return

    def reset(self, x, y):
        """
        Reset the puzzle to the initial state
        :param x: x-coordinate of the click, not used here
        :param y: y-coordinate of the click, not used here
        :return: None
        """
        self.clear_board()
        self.load_puzzle()
        self.empty_tile_position = self.find_empty_tile_position()
        self.solvable = 'Yes' if self.is_solvable() else 'No'
        self.draw_all()
        self.notify_move_callback('reset_solvable')

    def scramble(self):
        """
        Scramble the puzzle, by shuffling the tiles randomly. Resolvability is not guaranteed
        :return: None
        """
        # Flatten the 2D list of tiles
        tiles_lst = [tile for row in self.tiles for tile in row]
        random.shuffle(tiles_lst)  # Shuffle the tiles
        # Reconstruct the 2D list of tiles
        self.tiles = [tiles_lst[i:i + self.num_tiles] for i in range(0, len(tiles_lst), self.num_tiles)]
        # Update the current positions of the tiles
        for i in range(self.num_tiles):
            for j in range(self.num_tiles):
                self.tiles[i][j].curr_position = (i, j)
        self.empty_tile_position = self.find_empty_tile_position()

    def get_legal_moves(self):
        """
        Get the possible legal moves of the current empty tile
        :return: list of legal moves
        """
        legal_moves = []
        row, col = self.empty_tile_position
        # Find all possible legal moves and add them to the list
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
        """
        Scramble the puzzle, by reversely moving the empty tile randomly. Resolvability is guaranteed
        :return: None
        """
        moves = random.randint(5, 200)  # Randomly choose the number of moves
        for _ in range(moves):
            legal_moves = random.choice(self.get_legal_moves())  # Randomly choose a legal move from the list
            # Swap the tiles but not display them yet, to prevent flickering
            self.swap(legal_moves, self.empty_tile_position)
            self.empty_tile_position = legal_moves

    def move_puzzle(self, position):
        """
        Move the puzzle by swapping the empty tile with the clicked tile.
        :param position: a tuple of the position of the clicked tile
        :return: None
        """
        row, col = position
        empty_row, empty_col = self.empty_tile_position
        if abs(row - empty_row) + abs(col - empty_col) == 1:
            draw = self.swap(position, self.empty_tile_position)  # Swap the tiles and draw the two tiles only
            self.empty_tile_position = position
            start_x, start_y = self.start_pos()
            for tile in draw:
                x = start_x + tile.curr_position[1] * self.tile_size
                y = start_y - tile.curr_position[0] * self.tile_size
                tile.draw(x, y)
            turtle.update()
            # Notify the callback functions
            self.notify_move_callback('count_move')
            self.notify_move_callback('check_game_over')

    def swap(self, prev_pos, next_pos):
        """
        Swap the tiles of the puzzle. Also used for testing (test_module.py).
        :param prev_pos: previous position of the tile
        :param next_pos: next position of the tile
        :return: a list of tiles to draw
        """
        draw = []
        self.tiles[prev_pos[0]][prev_pos[1]], self.tiles[next_pos[0]][next_pos[1]] = \
            self.tiles[next_pos[0]][next_pos[1]], self.tiles[prev_pos[0]][prev_pos[1]]
        self.tiles[next_pos[0]][next_pos[1]].curr_position = next_pos
        self.tiles[prev_pos[0]][prev_pos[1]].curr_position = prev_pos
        draw.append(self.tiles[prev_pos[0]][prev_pos[1]])
        draw.append(self.tiles[next_pos[0]][next_pos[1]])
        return draw

    def calculate_inversions(self):
        """
        Calculate the number of inversions in the puzzle
        :return: inversions
        """
        """
        A inversion refers to a pair of tiles (a, b) where a appears before b but a > b.
        The number of inversions is used to determine if the puzzle is solvable.
        """
        inversions = 0
        # Flatten the 2D list of tiles
        tiles_lst = [tile for row in self.tiles for tile in row]
        # Calculate the number of inversions by arranging them in linear positions (excluding the empty tile)
        linear_positions = [tuple_to_linear_index(tile.init_position, self.num_tiles)
                            for tile in tiles_lst if tile.init_position != (self.num_tiles - 1, self.num_tiles - 1)]
        for i in range(len(linear_positions)):
            for j in range(i + 1, len(linear_positions)):
                if linear_positions[i] > linear_positions[j]:
                    inversions += 1
        return inversions

    def is_solvable(self):
        """
        Check if the puzzle is solvable
        :return: yes if solvable, no otherwise
        """
        """
        For puzzles with odd number of tiles, the puzzle is solvable if the number of inversions is even.
        For puzzles with even number of tiles, the puzzle is solvable:
            1. if the number of inversions is even and the row number of the empty tile counted from the bottom is odd.
            2. if the number of inversions is odd and the row number of the empty tile counted from the bottom is even.
        """
        inversions = self.calculate_inversions()
        if self.num_tiles % 2 != 0:
            return inversions % 2 == 0
        else:
            blank_row = self.num_tiles - self.empty_tile_position[0]
            if blank_row % 2 == 0:
                return inversions % 2 != 0
            else:
                return inversions % 2 == 0

    def is_solved(self):
        """
        Check if the puzzle is solved
        :return: True if solved, False otherwise
        """
        for row in self.tiles:
            for tile in row:
                if tile.curr_position == self.empty_tile_position:
                    continue
                if tile.init_position != tile.curr_position:
                    return False
        return True

    def find_empty_tile_position(self):
        """
        Find the position of the empty tile
        :return: current position of the empty tile
        """
        for row in self.tiles:
            for tile in row:
                if tile.init_position == (self.num_tiles - 1, self.num_tiles - 1):
                    return tile.curr_position

    def clear_board(self):
        """
        Clear the board
        :return: None
        """
        for row in self.tiles:
            for tile in row:
                tile.turtle.ht()
                tile.turtle = None

    def release_click(self):
        """
        Release all click events
        :return: None
        """
        for row in self.tiles:
            for tile in row:
                tile.turtle.onclick(None)
