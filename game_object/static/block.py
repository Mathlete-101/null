import random

import pygame

from game_object.game_object import GameObject
from tools import duple, transform
from tools.transform import MicroRect, rect_intersect


class Block(GameObject):

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        self._image = image
        self.render()


    def __init__(self, position, render_target, image):
        self._image: pygame.Surface = image
        if self._image:
            self._image.set_colorkey((255, 255, 255))
        self.location = position
        self.render_target = render_target
        self.render_position = duple.scale(position, 21 * 2)
        self.hitbox = pygame.Rect(self.render_position[0], self.render_position[1], 42, 42)
        self.render()
        self.tags = []
        self.is_floor = True
        self.is_ceiling = True
        self.is_left_wall = True
        self.is_right_wall = True
        self.opaque = True
        self.network = None

    def render(self):
        self.render_target.blit(transform.scale_factor(self.image, 2), self.render_position)

    def check_point_hit(self, position):
        return self.hitbox.collidepoint(position)

    def alert(self):
        r = random.randint(0, 255)
        surface = pygame.Surface((42, 42))
        surface.fill((r, 0, 0))
        if self.render_target:
            self.render_target.blit(surface, self.render_position)

    @property
    def micro_hitbox(self):
        return MicroRect(self.hitbox.x, self.hitbox.y, self.hitbox.w, self.hitbox.h)

    def check_box_intersection(self, hitbox: pygame.rect):
        return self.hitbox.colliderect(hitbox)

        # if position[0] > self.position[0] + 21 or position[1] > self.position[1] + 21:
        #     return False
        # if position[0] + len(hitbox) < self.position[0] or position[1] + len(hitbox[0]) < self.position:
        #     return False
        #
        # first_point = (position[0] - max(position[0], self.position[0]), position[1] - max(position[1], self.position[1]))
        # second_point = (position[0] - min(position[0] + len(hitbox), self.position[0] + 21), position[1] - min(position[1] + len(hitbox[0]), self.position[1] + 21))
        #
        # the_relevant_part = hitbox[first_point[0]:second_point[0], first_point[1]:second_point[1]]
        #
        # offset = ()
        #
        # for i in range(self.position[0], len(self.hitbox) + self.position[0]):
        #     for j in range(self.position[1], len(self.hitbox) + self.position[1]):
        #         pass

    def check_support(self, hitbox):
        first_check = self.check_box_intersection(hitbox.move(0, 0))
        second_check = self.check_box_intersection(hitbox.move(0, 1))
        return not first_check and second_check

    @property
    def special_collision(self):
        return False

    def collide_special(self, player):
        pass

    def init_collide_special(self, player):
        pass

    @property
    def x_center(self):
        return self.x + self.hitbox.width / 84

    @x_center.setter
    def x_center(self, val):
        self.x = val - self.hitbox.width / 84

