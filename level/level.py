from typing import List

from blocks.air import Air
from blocks.block import Block


def generate_blank_grid(dim):
    grid = []
    for i in range(0, dim[0]):
        row = []
        for j in range(0, dim[1]):
            row.append(Air((i * 21, j * 21)))
        grid.append(row)
    return grid


class Level:
    def __init__(self, dim):
        self.background: List[List[Block]] = generate_blank_grid(dim)
        self.main = generate_blank_grid(dim)
        self.foreground = generate_blank_grid(dim)
        self.dim = dim

    def set(self, location: (int, int), block):
        self.main[location[0]][location[1]] = block

    def set_background(self, location: (int, int), block):
        self.background[location] = block

    def set_foreground(self, location: (int, int), block):
        self.foreground[location] = block
