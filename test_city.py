import unittest
from City import City
from point import Point


class TestCityMethods(unittest.TestCase):  # pragma: no cover

    def test_add_point_to_city(self):
        city = City(Point(1, 2, 'red', [], False))
        point_to_add = Point(3, 4, 'red', [], False)
        city.add(point_to_add)
        self.assertTrue(city.in_city(point_to_add))

    def test_get_cycles(self):  # pragma: no cover
        city = City(Point(1, 2, 'red', [], False))
        point2 = Point(3, 4, 'red', [], False)
        point3 = Point(5, 6, 'red', [], False)
        city.add(point2)
        city.add(point3)
        cycles = city.get_cycles()
        self.assertIsNotNone(cycles)
        self.assertIsInstance(cycles, list)

    def test_rect_cords(self):  # pragma: no cover
        point1 = Point(1, 2, 'red', [], False)
        city = City(point1)
        point2 = Point(1, 3, 'red', [], False)
        point3 = Point(2, 3, 'red', [], False)
        point4 = Point(2, 1, 'red', [], False)
        city.add(point2)
        city.add(point3)
        city.add(point4)
        point1.next = [point2]
        point2.next = [point3]
        point3.next = [point4]
        point4.next = [point1]
        cycles = city.get_cycles()
        if cycles:
            rect_cords = city.rect_cords(cycles[0])
            self.assertIsNotNone(rect_cords)
            self.assertIsInstance(rect_cords, tuple)
            self.assertIsInstance(rect_cords[0], list)
            self.assertIsInstance(rect_cords[1], int)

    def test_group_cycles(self):  # pragma: no cover
        point1 = Point(1, 2, 'red', [], False)
        city = City(point1)
        point2 = Point(1, 3, 'red', [], False)
        point3 = Point(2, 3, 'red', [], False)
        point4 = Point(2, 1, 'red', [], False)
        point5 = Point(1, 4, 'red', [], False)
        point6 = Point(2, 4, 'red', [], False)
        city.add(point2)
        city.add(point3)
        city.add(point4)
        point1.next = [point2]
        point2.next = [point3, point5]
        point5.next = [point6]
        point6.next = [point3]
        point3.next = [point4]
        point4.next = [point1]
        cycles = city.get_cycles()
        if cycles:
            groups = city.group_cycles(cycles)
            self.assertIsNotNone(groups)
            self.assertIsInstance(groups, list)
            for group in groups:
                self.assertIsInstance(group, list)
                for cycle in group:
                    self.assertIsInstance(cycle, list)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()