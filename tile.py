import math


class Tile:
    def __init__(self, x, y, mat, val):
        self.x = x
        self.y = y
        self.type = mat
        self.radius = 53
        self.val = val
        self.thief = False

    def is_inside(self, pos):
        x = pos[0]
        y = pos[1]
        dist = round(math.sqrt(((x - self.x) ** 2) + ((y - self.y) ** 2)))
        if dist < self.radius:
            return True
        else:
            return False


def dist(x1, y1, x2, y2):
    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return distance
