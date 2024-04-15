import unittest
from board import Board


class TestSolvable(unittest.TestCase):
    """
    Test class for Board.is_solvable() method
    """
    board = Board()

    def setup(self):
        """Setting up the board for testing"""
        self.board.load_puzzle()
        self.board.empty_tile_position = self.board.find_empty_tile_position()

    def test_even_solvable(self):
        """Test when the number of tiles of the puzzle is even"""
        self.setup()
        self.assertTrue(self.board.is_solvable())

    def test_odd_solvable(self):
        """Test when the number of tiles of the puzzle is odd"""
        self.board = Board('luigi.puz')

        self.setup()
        self.assertTrue(self.board.is_solvable())

    def test_even_not_solvable(self):
        """Test when the number of tiles of the puzzle is even but the puzzle is not solvable"""
        self.setup()
        self.board.swap((2, 2), (2, 3))
        self.assertFalse(self.board.is_solvable())

        self.setup()
        self.board.swap((2, 0), (2, 3))
        self.assertFalse(self.board.is_solvable())

        self.setup()
        self.board.swap((1, 1), (1, 3))
        self.assertFalse(self.board.is_solvable())

        # Multiple legit moves
        self.setup()
        self.board.swap((3, 3), (2, 3))
        self.board.swap((1, 0), (1, 3))
        self.board.swap((1, 1), (1, 2))
        self.assertFalse(self.board.is_solvable())

    def test_odd_not_solvable(self):
        """Test when the number of tiles of the puzzle is odd but the puzzle is not solvable"""
        self.board = Board('luigi.puz')

        self.setup()
        self.board.swap((1, 1), (1, 2))
        self.assertFalse(self.board.is_solvable())

        self.setup()
        self.board.swap((1, 0), (1, 2))
        self.assertFalse(self.board.is_solvable())

        self.setup()
        self.board.swap((2, 2), (1, 2))
        self.board.swap((0, 2), (0, 0))
        self.board.swap((1, 0), (1, 1))
        self.board.swap((2, 0), (2, 2))
        self.assertFalse(self.board.is_solvable())


class TestScramble(unittest.TestCase):
    """
    Test class for Board.real_scramble() method
    """
    board = Board()

    def setup(self):
        """Setting up the board for testing"""
        self.board.load_puzzle()
        self.board.empty_tile_position = self.board.find_empty_tile_position()
        self.board.real_scramble()

    def test_scramble_solvable(self):
        """Test if the puzzle is solvable after scrambling, repeats 10 times"""
        repeats = 10
        for i in range(repeats):
            with self.subTest(i=i):
                self.setup()
                self.assertTrue(self.board.is_solvable())


if __name__ == "__main__":
    unittest.main()
