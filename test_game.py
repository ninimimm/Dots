import unittest
import tkinter as tk

from City import City
from Game import Game, Point

class TestGameMethods(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()

    def tearDown(self):
        self.root.destroy()

    def test_play(self):
        game = Game("some_mode", "", 2, 5, ["Player1", "Player2"], self.root)
        point1 = Point(40, 40, "RED", [], [])
        point2 = Point(120, 120, "BLUE", [], [])

        game.play(point1, True)
        self.assertIn(point1.position, game.dict_points)
        self.assertNotIn(point1.position, game.all_points)
        self.assertEqual(len(game.steps), 1)
        self.assertEqual(game.number, 1)

        game.play(point2, False)
        self.assertIn(point2.position, game.dict_points)
        self.assertNotIn(point2.position, game.all_points)
        self.assertEqual(len(game.steps), 1)
        self.assertEqual(game.number, 2)

        game.play(point1, True)
        self.assertEqual(len(game.steps), 1)
        self.assertEqual(game.number, 2)

    def test_create_point_when_no_city_exists(self):
        game = Game("some_mode", "", 2, 5, ["Player1", "Player2"], None)
        cell_size = 10
        point = Point(0, 0, "RED", [], [])

        game.create_point(point, cell_size)

        self.assertEqual(len(game.cities), 1)
        self.assertEqual(game.cities[0].color, "RED")
        self.assertIn(point, game.cities[0].points)

    def test_create_point_when_city_with_same_color_exists(self):
        game = Game("some_mode", "", 2, 5, ["Player1", "Player2"], None)
        cell_size = 10
        existing_city = City(Point(0, 0, "RED", [], []))
        game.cities.append(existing_city)
        point = Point(0, 10, "RED", [], [])

        game.create_point(point, cell_size)

        self.assertEqual(len(game.cities), 1)
        self.assertEqual(len(existing_city.points), 2)
        self.assertIn(point, existing_city.points)

    def test_create_point_when_multiple_cities_with_same_color_exist(self):
        game = Game("some_mode", "", 2, 5, ["Player1", "Player2"], None)
        cell_size = 10
        city1 = City(Point(0, 0, "RED", [], []))
        city2 = City(Point(10, 0, "RED", [], []))
        game.cities = [city1, city2]
        point = Point(0, 10, "RED", [], [])

        game.create_point(point, cell_size)

        self.assertEqual(len(game.cities), 2)
        self.assertEqual(len(city1.points), 2)
        self.assertIn(point, city1.points)

    def test_point_in_polygon_inside(self):
        # Тестирование метода point_in_polygon для точки внутри полигона
        game = Game("some_mode", "", 2, 5, ["Player1", "Player2"], self.root)

        # Предоставляем полигон и точку, которая находится внутри полигона
        poly = [(0, 0), (0, 2), (2, 2), (2, 0)]
        point_inside = (1, 1)

        result = game.point_in_polygon(point_inside, poly)

        # Ожидаем, что точка внутри полигона, поэтому результат должен быть True
        self.assertTrue(result)

    def test_point_in_polygon_outside(self):
        # Тестирование метода point_in_polygon для точки вне полигона
        game = Game("some_mode", "", 2, 5, ["Player1", "Player2"], self.root)

        # Предоставляем полигон и точку, которая находится вне полигона
        poly = [(0, 0), (0, 2), (2, 2), (2, 0)]
        point_outside = (3, 3)

        result = game.point_in_polygon(point_outside, poly)

        # Ожидаем, что точка вне полигона, поэтому результат должен быть False
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
