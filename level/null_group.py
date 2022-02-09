import math
import random

import pygame.sprite

from misc.wrapped_sprite import WrappedSprite
from tools import duple
from graphics import graphics

class NullGroup(pygame.sprite.Group):
    def __init__(self, position, height):
        super().__init__()
        self.position = position
        self.nulls = []
        for i in range(height):
            self.nulls.append(WrappedSprite(graphics.get("null").get(), duple.scale((position, i), 42)))

        random.shuffle(self.nulls)
        chunk_size = math.ceil(len(self.nulls) / 8)
        self.sub_groups = [self.nulls[n:n + chunk_size] for n in range(0, len(self.nulls), chunk_size)]
        self.group_on = 0

    def update(self):
        if self.group_on < 8:
            self.add(self.sub_groups[self.group_on])
            self.group_on += 1

