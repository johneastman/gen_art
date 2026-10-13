import unittest
from v2.api import Shape

class API_V2_Shape(unittest.TestCase):
    
    def test_center(self):
        test_cases = [
            (0, 0, 10, (5, 5)),
            (15, 20, 35, (32, 37))
        ]

        for x, y, size, expected in test_cases:
            s = Shape(x, y, size)
            self.assertEqual(s.center, expected)
