from graphics.graphic_class.reflection_sectional_switch_graphic import ReflectionSectionalSwitchGraphic
from graphics.graphic_class.sectional_switch_graphic import SectionalSwitchGraphic
import pygame


class RotationReflectionSectionalSwitchGraphic(ReflectionSectionalSwitchGraphic):
    def __init__(self, on, off, sections, reflected=False, rotation=0):
        super().__init__(on, off, sections, reflected=reflected)
        self.rotation = rotation
        self.class_ = RotationReflectionSectionalSwitchGraphic

    def get_rotation(self, angle):
        return self.class_(self.on, self.off, self.sections, reflected=self.reflected, rotation=angle)

    def get_new_img(self, switches):
        return pygame.transform.rotate(super().get_new_img(switches), self.rotation * 90)




