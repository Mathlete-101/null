import pygame

from graphics.graphic_class.graphic import Graphic


class ReflectionGraphic(Graphic):
    def get_reflected(self, y=True, x=False):
        return pygame.transform.flip(self.get(), y, x)