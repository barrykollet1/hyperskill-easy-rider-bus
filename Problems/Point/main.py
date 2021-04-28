import math


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, p):
        a = p.x
        b = p.y
        return math.sqrt((self.x - a) ** 2 + (self.y - b)**2)

