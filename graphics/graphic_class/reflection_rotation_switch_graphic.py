import pygame

from graphics.graphic_class.rotation_switch_graphic import RotationSwitchGraphic


# unused
class RotationReflectionSwitchGraphic(RotationSwitchGraphic):
    def get_rotation(self, angle):
        return RotationSwitchGraphic(pygame.transform.rotate(self.off, angle), pygame.transform.rotate(self.on, angle))

    def rotate(self, angle):
        rotation = self.get_rotation(angle)
        self.off = rotation.off
        self.on = rotation.on
