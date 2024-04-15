from file_manager import FileManager


class Leaderboard:
    """
    Leaderboard class to manage the leaderboard file.

    Attributes:
    file_manager (FileManager): FileManager object to manage the file.
    leaderboard_path (str): Path to the leaderboard file.
    leaderboard_path (dict): Dictionary of the leaderboard.
    """
    def __init__(self):
        """
        Constructor of the Leaderboard class.
        """
        self.file_manager = FileManager()
        self.leaderboard_path = self.file_manager.leaderboard_path
        self.leaderboard = self.file_manager.load_leaderboard_file()

    def leaderboard_text(self):
        """
        Method to create the leaderboard text.
        :return: returns the leaderboard text.
        """
        leaderboard_text = "Leader:\n\n\n"
        # Display the top 10 players in the leaderboard
        for i in range(0, 10):
            if i < len(self.leaderboard):
                # Truncate the player name if it is longer than 8 characters
                if len(list(self.leaderboard)[i]) > 8:
                    player_name = list(self.leaderboard)[i][0:8] + '... '
                else:
                    player_name = list(self.leaderboard)[i]
                leaderboard_text += f"{player_name}: {list(self.leaderboard.values())[i]}\n\n"
            else:
                leaderboard_text += "\n\n"
        return leaderboard_text

    def write_leaderboard(self, player_name, total_move):
        """
        Method to write the leaderboard file.
        :param player_name: Name of the player
        :param total_move: Number of moves of the player
        :return: None
        """
        self.file_manager.write_leaderboard_file(player_name, total_move)
