import pygame

from blocks.block import Block


class Air(Block):

    def __init__(self, position, image=None):
        super().__init__(position, image)
        self.image = pygame.Surface((0, 0))
        self.image.set_alpha(0)

    def check_point_hit(self, position):
        return False

    def check_box_intersection(self, hitbox: pygame.Rect):
        return False

    def check_support(self, hitbox):
        return False

