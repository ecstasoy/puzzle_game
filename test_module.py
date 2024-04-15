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
        """
        | 0 | 1 | 2 | 3 |
        | 4 | 5 | 6 | 7 |
        | 8 | 9 | 10| 11|
        | 12| 13| 14|   |
        
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        Blank tile is at (3, 3), omitted in the list
        
        Inversions: 0
        Blank tile row from the bottom: 1
        """
        self.setup()
        self.assertTrue(self.board.is_solvable())

    def test_odd_solvable(self):
        """Test when the number of tiles of the puzzle is odd"""
        """
        | 0 | 1 | 2 |
        | 3 | 4 | 5 |
        | 6 | 7 |   |
        
        [0, 1, 2, 3, 4, 5, 6, 7]
        Blank tile is at (2, 2), omitted in the list
        
        Inversions: 0
        """
        self.board = Board('luigi.puz')

        self.setup()
        self.assertTrue(self.board.is_solvable())

    def test_even_not_solvable(self):
        """Test when the number of tiles of the puzzle is even but the puzzle is not solvable"""
        """
        | 0 | 1 | 2 | 3 |
        | 4 | 5 | 6 | 7 |
        | 8 | 9 | 11| 10|
        | 12| 13| 14|   |
        
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 10, 12, 13, 14]
        Blank tile is at (3, 3), omitted in the list
        
        Inversions: 1
        Blank tile row from the bottom: 1
        
        They are both odd, so the puzzle is not solvable
        """
        self.setup()
        self.board.swap((2, 2), (2, 3))
        self.assertFalse(self.board.is_solvable())

        """
        | 0 | 1 | 2 | 3 |
        | 4 | 5 | 6 | 7 |
        | 11| 9 | 10| 8 |
        | 12| 13| 14|   |

        [0, 1, 2, 3, 4, 5, 6, 7, 11, 9, 10, 8, 12, 13, 14]
        Blank tile is at (3, 3), omitted in the list

        Inversions: 5
        Blank tile row from the bottom: 1

        They are both odd, so the puzzle is not solvable
        """
        self.setup()
        self.board.swap((2, 0), (2, 3))
        self.assertFalse(self.board.is_solvable())

        """
        | 0 | 1 | 2 | 3 |
        | 7 | 5 | 6 | 4 |
        | 8 | 9 | 11| 10|
        | 12| 13| 14|   |

        [0, 1, 2, 3, 7, 5, 6, 4, 8, 9, 11, 10, 12, 13, 14]
        Blank tile is at (3, 3), omitted in the list

        Inversions: 5
        Blank tile row from the bottom: 1

        They are both odd, so the puzzle is not solvable
        """
        self.setup()
        self.board.swap((1, 1), (1, 3))
        self.assertFalse(self.board.is_solvable())

        """
        | 0 | 1 | 2 | 3 |
        | 7 | 6 | 5 | 4 |
        | 8 | 9 | 11|   |
        | 12| 13| 14| 10|

        [0, 1, 2, 3, 7, 5, 6, 4, 8, 9, 11, 10, 12, 13, 14]
        Blank tile is at (2, 3), omitted in the list

        Inversions: 10
        Blank tile row from the bottom: 2

        They are both even, so the puzzle is not solvable
        """
        # Multiple legit moves
        self.setup()
        self.board.swap((3, 3), (2, 3))
        self.board.swap((1, 0), (1, 3))
        self.board.swap((1, 1), (1, 2))
        self.assertFalse(self.board.is_solvable())

    def test_odd_not_solvable(self):
        """Test when the number of tiles of the puzzle is odd but the puzzle is not solvable"""
        self.board = Board('luigi.puz')

        """
        | 0 | 1 | 2 |
        | 3 | 5 | 4 |
        | 6 | 7 |   |
        
        [0, 1, 2, 3, 5, 4, 6, 7]
        Blank tile is at (2, 2), omitted in the list
        
        Inversions: 1
        
        Inversions is odd, so the puzzle is not solvable
        """
        self.setup()
        self.board.swap((1, 1), (1, 2))
        self.assertFalse(self.board.is_solvable())

        """
        | 0 | 1 | 2 |
        | 5 | 4 | 3 |
        | 6 | 7 |   |

        [0, 1, 2, 5, 4, 3, 6, 7]
        Blank tile is at (2, 2), omitted in the list

        Inversions: 3

        Inversions is odd, so the puzzle is not solvable
        """
        self.setup()
        self.board.swap((1, 0), (1, 2))
        self.assertFalse(self.board.is_solvable())

        """
        | 2 | 1 | 0 |
        | 4 | 3 |   |
        | 5 | 7 | 6 |

        [2, 1, 0, 5, 4, 6, 8, 7]
        Blank tile is at (1, 2), omitted in the list

        Inversions: 5

        Inversions is odd, so the puzzle is not solvable
        """
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
