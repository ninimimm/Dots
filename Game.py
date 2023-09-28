import json
import tkinter as tk

from point import Point
from City import City
from PC import PC


class Game:
    def __init__(self, mode, computer_difficulty, count_players, map_grid, player_names, root):
        self.root = root
        self.width = 800
        self.height = 800
        self.mode = mode
        self.count_players = count_players
        self.map_grid = map_grid
        self.cell_size = 800 // map_grid
        self.computer_difficulty = computer_difficulty
        self.point_size = self.cell_size // 5
        self.canvas = tk.Canvas(root, width=self.width, height=self.height)
        self.canvas.grid(row=0, column=0)
        self.canvas.bind('<Button-1>', self.on_click)
        self.people_colors =["RED", "BLUE", "GREEN", "ORANGE"]
        self.people_scores = [0, 0, 0, 0]
        self.current_color = None
        self.dict_points = {}
        self.captured_points = {}
        self.ban_points =[set(), set(), set(), set()][:self.count_players]
        self.cities = []  # Use a list to store cities
        self.create_grid()
        self.number = 0
        self.player_names = player_names
        self.score_labels = []
        self.load_scores_from_json("scores.json")
        if self.tabel == None:
            self.tabel = {}
        self.draw_score()
        self.all_points = set()
        self.steps = []
        if computer_difficulty != "":
            self.pc = PC()
            for col in range(1, map_grid+1):
                for row in range(map_grid):
                    self.all_points.add((col * self.cell_size - self.point_size / 2, (
                            row + 0.5) * self.cell_size - self.point_size / 2))

    def draw_score(self):
        self.scores_frame = tk.Frame(self.root)
        self.scores_frame.grid(row=0, column=0, sticky='e')  # Align to the left

        # Create a label to display people_scores with an increased font size
        self.scores_label = tk.Label(self.scores_frame, text="Счет:", font=("Helvetica", 20),
                                     anchor='w')  # Anchor to the left
        self.scores_label.grid(row=0, column=0, sticky='w')  # Align to the left within scores_frame

        # Create labels for each player's score with an increased font size

        for i in range(self.count_players):
            score_label = tk.Label(self.scores_frame, text=f"{self.player_names[i]}: 0", font=("Helvetica", 18),
                                   anchor='w')  # Anchor to the left
            score_label.grid(row=i + 1, column=0, padx=10,
                             sticky='w')  # Align to the left within scores_frame, Adjust padx as needed
            self.score_labels.append(score_label)

    def save_scores_to_json(self, file_path):
        # Сохранить счеты в JSON файл
        with open(file_path, "w") as json_file:
            json.dump(self.tabel, json_file)

    def load_scores_from_json(self, file_path):
        # Загрузить счеты из JSON файла
        with open(file_path, "r") as json_file:
            self.tabel = json.load(json_file)

    def play(self, point, is_player):
        if point.position not in self.dict_points and all(point.position not in x for x in self.ban_points):
            if len(self.all_points) > 0: self.all_points.remove(point.position)
            self.create_point(point, self.cell_size)
            self.dict_points[point.position] = (point.color, point)
            if self.computer_difficulty == "": self.number += 1
            if is_player: self.steps.append(point.position)

            self.draw_point(point.position[0], point.position[1], self.dict_points[point.position][0])
            for city in self.cities:
                if city is not None:
                    for group in city.group_cycles(city.get_cycles()):
                        sort_group = sorted(group, key=lambda x: (self.diff(city.rect_cords(x), x, x[0])))
                        df = self.diff(city.rect_cords(sort_group[0]), sort_group[0], sort_group[0][0])
                        if df[0] != 0:
                            for i in range(self.count_players):
                                self.people_scores[i] = len([x for x in self.ban_points[i] if self.dict_points[x][0] !=
                                                             self.people_colors[i]])
                            self.draw_polygon(sort_group[0])

                            array = self.array_points_inside(city.rect_cords(sort_group[0]), sort_group[0])
                            for pt in array:
                                if pt not in self.captured_points:
                                    self.captured_points[pt] = self.number % self.count_players
                                else:
                                    self.captured_points[pt] = self.number % self.count_players
                                for end in self.dict_points[pt][1].end:
                                    if end is None: continue
                                    for j in range(len(end.next)):
                                        if end.next[j] is not None and pt == end.next[j].position:
                                            end.next[j] = None
                            for ct in self.cities:
                                if ct is None: continue
                                for k in range(len(ct.points)):
                                    if k is not None:
                                        for pt in array:
                                            if ct.points[k] is not None and ct.points[k].position == pt:
                                                ct.points[k] = None
        for i in range(len(self.score_labels)):
            self.score_labels[i].config(text=f"{self.player_names[i]}: {self.people_scores[i]}")
        for i in range(self.count_players):
            if self.player_names[i] in self.tabel:
                self.tabel[self.player_names[i]] = max(self.tabel[self.player_names[i]], self.people_scores[i])
            else:
                self.tabel[self.player_names[i]] = self.people_scores[i]
            self.save_scores_to_json("scores.json")
        self.clear_cities()



    def on_click(self, event):
        if self.computer_difficulty == "":
            point = self.click(event)
            self.play(point, True)
        else:
            point = self.click(event)
            self.play(point, True)
            if self.computer_difficulty == "Рандомный":
                point = self.pc.random(self.all_points)
            elif self.computer_difficulty == "Сложный":
                point = self.pc.brain(self.all_points, self.steps, self.dict_points, self.cell_size)
            self.play(point, False)

    def click(self, event):
        self.current_color = self.people_colors[self.number % self.count_players]
        x, y = event.x, event.y
        col, row = (x + self.cell_size // 2) // self.cell_size, y // self.cell_size
        center_x, center_y = col * self.cell_size - self.point_size / 2, (
                row + 0.5) * self.cell_size - self.point_size / 2
        return Point(int(center_x), int(center_y), self.current_color, [], [])


    def draw_polygon(self, cycle):
        points = [(point[0] + self.point_size // 2, point[1] + self.point_size // 2) for point in cycle]
        polygon = self.canvas.create_polygon(points, fill=self.dict_points[cycle[0]][0].lower(), outline=self.dict_points[cycle[0]][0].lower(), stipple="gray50")
        self.canvas.tag_lower(polygon)

    def create_point(self, point, cell_size):
        count = 0
        for city in self.cities:
            if city == None or point.color != city.color:
                continue
            flag = False
            for pt in city.points:
                if pt is not None:
                    if pt.position[0] == point.position[0] - cell_size and pt.position[1] in (
                    point.position[1] + cell_size, point.position[1] - cell_size, point.position[1]) or\
                        pt.position[0] == point.position[0] and pt.position[1] in (
                    point.position[1] + cell_size, point.position[1] - cell_size) or\
                        pt.position[0] == point.position[0] + cell_size and pt.position[1] in (
                    point.position[1] + cell_size, point.position[1] - cell_size, point.position[1]):
                        pt.next.append(point)
                        pt.end.append(point)
                        point.end.append(pt)
                        point.next.append(pt)
                        flag = True
            if flag:
                city.add(point)
                count += 1
        if count == 0:
            city = City(point)
            self.cities.append(city)
        elif count > 1:
            last = 0
            for i in range(len(self.cities)):
                if self.cities[i] != None and self.cities[i].in_city(point):
                    if last == 0: last = i
                    else:
                        for m in range(len(self.cities[last].points)):
                            if self.cities[last].points[m] is not None and not(self.cities[i].in_city(self.cities[last].points[m])):
                                self.cities[i].add(self.cities[last].points[m])
                        self.cities[last] = None
                        last = i
    def diff(self, data, cycle, pt):
        plus, minus = 0, 0
        for point in self.array_points_inside(data, cycle):
            for k in range(len(self.ban_points)):
                if self.people_colors[k] != self.dict_points[pt][0] and point in self.ban_points[k]:
                    self.ban_points[k].remove(point)
            self.ban_points[[x for x in range(len(self.people_colors)) if self.people_colors[x] == self.dict_points[pt][0]][0]].add(point)
            if self.dict_points[point][0] == self.dict_points[cycle[0]][0]:
                minus += 1
            else: plus += 1
        return (-plus, minus, data[1])

    def array_points_inside(self, data, cycle):
        rect = data[0]
        ans = []
        for x in range(rect[0]+self.cell_size, rect[2], self.cell_size):
            for y in range(rect[1]+self.cell_size, rect[3], self.cell_size):
                if (x, y) in self.dict_points and (x, y) not in cycle and self.point_in_polygon((x, y), cycle):
                    ans.append((x, y))
        return ans

    def create_grid(self):
        for i in range(1, self.map_grid + 1):
            y = i * self.cell_size
            self.canvas.create_line(self.cell_size, y - self.cell_size // 2, self.map_grid * self.cell_size, y - self.cell_size // 2)
            self.canvas.create_line(y, self.cell_size // 2, y, self.map_grid * self.cell_size - self.cell_size // 2)

    def draw_point(self, row, col, color):
        self.canvas.create_oval(row, col, row + self.point_size, col + self.point_size, fill=color)

    def point_in_polygon(self, point, poly):
        x, y = point
        path_length = len(poly)
        j = path_length - 1
        is_inside = False
        for i in range(path_length):
            if ((poly[i][1] > y) != (poly[j][1] > y)) and \
                    (x < poly[i][0] + (poly[j][0] - poly[i][0]) * (y - poly[i][1]) / (poly[j][1] - poly[i][1])):
                is_inside = not is_inside
            j = i
        return is_inside

    def clear_cities(self):
        for city in self.cities:
            if city is None: continue
            for i in range(len(city.points)):
                if city.points[i] is None: continue
                if city.points[i].position[0] == self.cell_size - self.point_size / 2 \
                    or city.points[i].position[1] == (0 + 0.5) * self.cell_size - self.point_size / 2\
                    or city.points[i].position[0] == self.map_grid * self.cell_size - self.point_size/ 2 \
                    or city.points[i].position[1] == (self.map_grid - 1 + 0.5) * self.cell_size - self.point_size/ 2:

                    if city.points[i].position[0] == self.cell_size - self.point_size / 2 \
                    and city.points[i].position[1] == (0 + 0.5) * self.cell_size - self.point_size / 2\
                    or city.points[i].position[0] == self.cell_size - self.point_size / 2 \
                    and city.points[i].position[1] == (self.map_grid - 1 + 0.5) * self.cell_size - self.point_size / 2\
                    or city.points[i].position[0] == self.map_grid * self.cell_size - self.point_size/ 2 \
                    and city.points[i].position[1] == (0 + 0.5) * self.cell_size - self.point_size/ 2\
                    or city.points[i].position[0] == self.map_grid * self.cell_size - self.point_size/ 2 \
                    and city.points[i].position[1] == (self.map_grid - 1 + 0.5) * self.cell_size - self.point_size/ 2:
                        if len(city.points[i].next) == 3:
                            self.help_clear(city, i)
                    elif len(city.points[i].next) == 5:
                        self.help_clear(city, i)
                elif len(city.points[i].next) == 8:
                    self.help_clear(city, i)

    def help_clear(self, city, i):
        for j in range(len(city.points[i].end)):
            if city.points[i].end[j] is None: continue
            for l in range(len(city.points[i].end[j].next)):
                if city.points[i].end[j].next[l] is None: continue
                if city.points[i].end[j].next[l].position == city.points[i].position:
                    city.points[i].end[j].next[l] = None
            city.points[i].end[j] = None
        for j in range(len(city.points[i].next)):
            if city.points[i].next[j] is None: continue
            for l in range(len(city.points[i].next[j].next)):
                if city.points[i].next[j].next[l] is None: continue
                if city.points[i].next[j].next[l].position == city.points[i].position:
                    city.points[i].next[j].next[l] = None
            city.points[i].end[j] = None
        city.points[i] = None