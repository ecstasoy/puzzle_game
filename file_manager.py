import os
import datetime
import inspect


class FileManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(FileManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, puzzle_file='mario.puz', leaderboard_path='leaderboard.txt',
                 error_log_path='', log_file='5001_puzzle.err'):
        if not hasattr(self, 'initialized'):
            self.puzzle_file = puzzle_file
            self.leaderboard_path = leaderboard_path
            self.error_log_path = error_log_path
            self.log_file = log_file
            self.initialize = True

    def log_error(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        caller_function = inspect.stack()[1].function
        formatted_msg = f"{timestamp} ERROR: {message}LOCATION: {caller_function}\n"
        with open(self.log_file, 'a') as log:
            log.write(formatted_msg)

    def load_puzzle_file(self):
        puzzle_config = {}
        try:
            with open(f"{self.puzzle_file}", 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if line.strip() == '':
                        continue
                    key, value = line.strip().split(': ')
                    if key.isdigit():
                        puzzle_config[int(key)] = value.strip()
                    elif value.isdigit():
                        puzzle_config[key] = int(value.strip())
                    else:
                        puzzle_config[key] = value.strip()
        except FileNotFoundError as e:
            self.log_error(f"Puzzle file not found - \"{self.puzzle_file}\" - {e} ")
        except ValueError as e:
            self.log_error(f"Value error - {e} ")
        return puzzle_config

    def load_leaderboard_file(self):
        leaderboard = {}

        try:
            with open(self.leaderboard_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    if line:
                        player, score = line.split(',')
                        leaderboard[player] = int(score)
        except FileNotFoundError as e:
            self.log_error(f"Leaderboard file not found - \"{self.leaderboard_path}\" - {e}\n"
                           f"leaderboard.txt created\n ")
            with open(self.leaderboard_path, 'w') as file:
                file.write("")

        leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1]))
        return leaderboard

    def write_leaderboard_file(self, player_name, total_move):
        try:
            with open(self.leaderboard_path, 'a') as file:
                file.write(f"\n{player_name},{total_move}")
        except FileNotFoundError as e:
            self.log_error(f"Leaderboard file not found - \"{self.leaderboard_path}\" - {e}\n"
                           f"leaderboard.txt created\n ")
            with open(self.leaderboard_path, 'w') as file:
                file.write(f"\n{player_name},{total_move}")

    def check_puzzle_config(self, file_name):
        prev = self.puzzle_file
        self.puzzle_file = file_name
        puzzle_config = self.load_puzzle_file()
        if not os.path.isfile(puzzle_config['thumbnail']):
            self.puzzle_file = prev
            self.log_error(f"Malformed puzzle file - \"{file_name}\" "
                           f"Path does not exist - \"{puzzle_config['thumbnail']}\"")
            return False
        num_tiles = puzzle_config['number']
        for i in range(1, num_tiles + 1):
            image_path = puzzle_config.get(i)
            if not os.path.isfile(image_path):
                self.puzzle_file = prev
                self.log_error(f"Malformed puzzle file - \"{file_name}\" "
                               f"Path does not exist - \"{image_path}\"")
                return False
        return True

    def load_puzzle_catalog(self):
        puzzle_catalog = []
        for file in os.listdir():
            if file.endswith('.puz'):
                puzzle_catalog.append(file)
        return puzzle_catalog
