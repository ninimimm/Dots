import random
from point import Point
class PC:
    def __init__(self):
        pass

    def random(self, all_points):
        pt = random.choice([x for x in all_points])
        return Point(pt[0], pt[1], "BLUE", [], [])
    def brain(self, all_points, steps, dict_points, cell_size):
        index = len(steps)-1
        ans = None
        while index >= 0:
            pt = steps[index]
            k = set()
            neighbors = [
                (pt[0] + cell_size, pt[1]),
                (pt[0] - cell_size, pt[1]),
                (pt[0], pt[1] + cell_size),
                (pt[0], pt[1] - cell_size),
                (pt[0] + cell_size, pt[1] + cell_size),
                (pt[0] - cell_size, pt[1] - cell_size),
                (pt[0] + cell_size, pt[1] - cell_size),
                (pt[0] - cell_size, pt[1] + cell_size),
            ]
            for l in neighbors:
                k.add(l)
            points_outside1 = [x for x in neighbors if x in all_points]
            points_outside2 = [x for x in neighbors if x in dict_points]
            flag_blue = False
            for pt in points_outside1:
                for point in points_outside2:
                    if pt == point: continue
                    if dict_points[point][0] == "BLUE":
                        flag_blue = True
                ans = pt
                if flag_blue: break
            if flag_blue: break
            index -= 1
        return Point(ans[0], ans[1], "BLUE", [], [])



