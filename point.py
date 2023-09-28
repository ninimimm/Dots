class Point:
    def __init__(self, x, y, color, next, end):
        self.position = (x, y)
        self.color = color
        self.next = next
        self.end = end

    def __eq__(self, other):
        return self.position == other.position and self.color == other.color

    def __hash__(self):
        return hash((self.position, self.color))