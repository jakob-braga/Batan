from tile import *
from setup import *


class Settlement:
    def __init__(self, pos):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.level = 1
        self.radius = 65
        self.local_radius = 13

    def is_inside(self, pos):
        if dist(self.x, self.y, pos[0], pos[1]) < self.radius:
            return True
        else:
            return False

    def is_inside_local(self, pos):
        return dist(self.x, self.y, pos[0], pos[1]) < self.local_radius


class Road:
    def __init__(self, pos1):
        self.pos1 = pos1
        self.x1 = pos1[0]
        self.y1 = pos1[1]
        self.pos2 = None
        self.radius = 13

    def set_pos2(self, pos2):
        self.pos2 = pos2

    def is_inside_local(self, own_pos, pos):
        if own_pos == 1:
            return dist(self.x1, self.y1, pos[0], pos[1]) < self.radius
        else:
            return dist(self.pos2[0],self.pos2[1], pos[0], pos[1]) < self.radius
