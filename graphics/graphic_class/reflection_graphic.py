import pygame

from graphics.graphic_class.graphic import Graphic


class ReflectionGraphic(Graphic):
    def get_reflected(self):
        return pygame.transform.flip(self.get(), True, False)