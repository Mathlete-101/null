import pygame

from game_object.static.no_collision_block import NoCollisionBlock


class Air(NoCollisionBlock):

    def __init__(self, position, render_target=None, image=None):
        super().__init__(position, render_target, image)
        self.image = pygame.Surface((0, 0))
        self.image.set_alpha(0)
        self.tags.append("air")

    def render(self):
        pass

    def check_point_hit(self, position):
        return False

    def check_box_intersection(self, hitbox: pygame.Rect):
        return False

    def check_support(self, hitbox):
        return False
