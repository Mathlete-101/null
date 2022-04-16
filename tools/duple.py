import math


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def subtract(a, b):
    return a[0] - b[0], a[1] - b[1]


def scale(a, b):
    return a[0] * b, a[1] * b


def floor(a):
    return math.floor(a[0]), math.floor(a[1])


def near(a, b):
    return abs(a[0] - b[0]) <= 1 and abs(a[1] - b[1]) <= 1


def adjacent(a, b):
    return abs(a[0] - b[0]) == 1 and a[1] == b[1] or abs(a[1] - b[1]) == 1 and a[0] == b[0]


def insert(a, b):
    return a[0], b


def d_round(a):
    return round(a[0]), round(a[1])


def inner_multiply(a, b):
    return a[0] * b[0], a[1] * b[1]


class ScreenPosition:
    def __init__(self, dim):
        self.dim = dim

    def __call__(self, pos):
        return inner_multiply(pos, self.dim)