import unittest
from boggle import *

class TestBoggleMoves(unittest.TestCase):
    
    def setUp(self):
        self.officialBoard = [
            ['X', 'G', 'T', 'S'],
            ['A', 'M', 'Z', 'J'],
            ['E', 'O', 'C', 'M'],
            ['U', 'F', 'E', 'V']
        ]

        self.testBoard = [
            ['J', 'O', 'P', 'Y'],
            ['C', 'M', 'P', 'V'],
            ['X', 'F', 'E', 'G'],
            ['P', 'G', 'V', 'U']
        ]
    
    def test_possible_moves_corner(self):
        expected = {(0, 1), (1, 0), (1, 1)}
        result = set(possibleMoves((0, 0), self.officialBoard))
        self.assertEqual(result, expected)
    
    def test_possible_moves_center(self):
        expected = {(1, 2), (3, 2), (1, 3), (3, 3), (3, 1), (2, 1), (2, 3), (1, 1)}
        result = set(possibleMoves((2, 2), self.officialBoard))
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
