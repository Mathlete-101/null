import pygame.transform

from graphics.graphic_class.graphic import Graphic


class RotationGraphic(Graphic):
    def get_rotation(self, angle):
        return pygame.transform.rotate(self.img, angle)