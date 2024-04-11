from file_manager import FileManager


class Leaderboard:
    def __init__(self):
        self.file_manager = FileManager()
        self.leaderboard_path = self.file_manager.leaderboard_path
        self.leaderboard = self.file_manager.load_leaderboard_file()

    def leaderboard_text(self):
        leaderboard_text = "Leader:\n\n\n"
        player_name = ''
        for i in range(0, 10):
            if i < len(self.leaderboard):
                if len(list(self.leaderboard)[i]) > 8:
                    player_name = list(self.leaderboard)[i][0:8] + '... '
                else:
                    player_name = list(self.leaderboard)[i]
                leaderboard_text += f"{player_name}: {list(self.leaderboard.values())[i]}\n\n"
            else:
                leaderboard_text += "\n\n"
        return leaderboard_text

    def write_leaderboard(self, player_name, total_move):
        self.file_manager.write_leaderboard_file(player_name, total_move)
