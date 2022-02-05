from graphics.graphic_class.switch_graphic import SwitchGraphic
import pygame


class RotationSwitchGraphic(SwitchGraphic):
    def get_rotation(self, angle):
        return RotationSwitchGraphic(pygame.transform.rotate(self.off, angle), pygame.transform.rotate(self.on, angle))

    def rotate(self, angle):
        rotation = self.get_rotation(angle)
        self.off = rotation.off
        self.on = rotation.on
