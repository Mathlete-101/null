import pygame.transform

from graphics.graphic_class.graphic import Graphic


class RotationGraphic(Graphic):
    def get_rotation(self, angle):
        copy = self.get().copy()
        return pygame.transform.rotate(copy, angle)