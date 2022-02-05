import tools.lists
from graphics.graphic_class.graphic import Graphic
import pygame


class SectionalSwitchGraphic(Graphic):
    def get_switch_val(self):
        # this requires the bitarray module which we don't yet have access to
        pass

    def __init__(self, off, on, sections):
        super().__init__(off)
        self.on = on
        self.off = off
        self.sections = sections
        self.table = {}

    def get_sectional(self, switches) -> pygame.Surface:
        hash_ = tools.lists.hash_bit_array(switches)
        if hash_ not in self.table:
            self.table[hash_] = self.get_new_img(switches)

        return self.table[hash_]

    def get_new_img(self, switches):
        new_img: pygame.Surface = self.off.copy()
        for i in range(len(switches)):
            if switches[i]:
                new_img.blit(self.sections[i], (0, 0))
        return new_img

