import unittest
from PC import PC
from point import Point


class TestPCMethods(unittest.TestCase):  # pragma: no cover

    def setUp(self):  # pragma: no cover
        self.pc = PC()

    def test_random(self):  # pragma: no cover
        all_points = [(0, 0), (1, 1), (2, 2), (3, 3)]
        result = self.pc.random(all_points)
        self.assertIsInstance(result, Point)
        self.assertTrue(result.position in all_points)
        self.assertEqual(result.color, "BLUE")

    def test_brain(self):  # pragma: no cover
        all_points = [(0, 0), (1, 1), (2, 2), (3, 3)]
        steps = [(1, 1), (2, 2), (3, 3)]
        dict_points = {(1, 1): ["RED", []], (2, 2): ["GREEN", []]}
        cell_size = 1

        result = self.pc.brain(all_points, steps, dict_points, cell_size)
        self.assertIsInstance(result, Point)
        self.assertTrue(result.position not in [(3, 2), (2, 3), (4, 3), (3, 4)])
        self.assertEqual(result.color, "BLUE")


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
