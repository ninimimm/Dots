class City:
    def __init__(self, point):
        self.points = [point]
        self.color = point.color
        self.set_position = set()
        self.set_position.add(point.position)

    def add(self, point):
        if point.position not in self.set_position:
            self.points.append(point)
            self.set_position.add(point.position)

    def in_city(self, point):
        return point.position in self.set_position

    def get_cycles(self):
        cycles = []
        visited = set()

        def dfs_cycle(current_point, path, k):
            visited.add(current_point)
            path.append(current_point)

            for next_point in current_point.next:
                if next_point is not None and next_point.position in k:
                    path_cylce = [next_point]
                    index = len(path) - 1
                    while path[index].position != next_point.position:
                        path_cylce.append(path[index])
                        index -= 1
                        if index < 0: break
                    if index >= 0 and len(path_cylce) > 3:
                        cycles.append([x.position for x in path_cylce])

            for next_point in current_point.next:
                if next_point is not None and next_point not in visited:
                    k.add(next_point.position)
                    dfs_cycle(next_point, path, k)

            path.pop()
            visited.remove(current_point)

        for point in self.points:
            if point is not None:
                h = set()
                h.add(point.position)
                dfs_cycle(point, [point], h)
                break
        return cycles

    def rect_cords(self, cycle):
        min_x, max_x, min_y, max_y = 10**9, 0, 10**9, 0
        for point in cycle:
            min_x = min(min_x, point[0])
            max_x = max(max_x, point[0])
            min_y = min(min_y, point[1])
            max_y = max(max_y, point[1])

        return ([int(x) for x in [min_x, min_y, max_x, max_y]], len(cycle))

    def group_cycles(self, cycles):
        cycles = sorted(cycles, key=len, reverse=True)
        groups = []

        for cycle in cycles:
            add = True
            for group in groups:
                added_to_group = True
                for point in cycle:
                    if point not in group[0]:
                        added_to_group = False
                if added_to_group:
                    add = False
                    if len(cycle) != len(group[0]):
                        group.append(cycle)
                        break
            if add:groups.append([cycle])
        return groups