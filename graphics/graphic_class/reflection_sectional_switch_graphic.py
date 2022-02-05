from graphics.graphic_class.sectional_switch_graphic import SectionalSwitchGraphic
import pygame


class ReflectionSectionalSwitchGraphic(SectionalSwitchGraphic):
    def __init__(self, on, off, sections, reflected=False):
        super().__init__(on, off, sections)
        self.reflected = reflected
        self.class_ = ReflectionSectionalSwitchGraphic

    def get_reflection(self, reflected=True):
        return self.class_(self.on, self.off, self.sections, reflected=not (self.reflected == reflected))

    def get_new_img(self, switches):
        return pygame.transform.flip(super().get_new_img(switches), flip_y=self.reflected, flip_x=False)
