import pygame


class Block:
    def __init__(self, position, image):
        self.image = image
        self.position = position
        self.hitbox = pygame.Rect(position[0], position[1], 21, 21)

    def render(self):
        return self.image

    def check_point_hit(self, position):
        return self.hitbox.collidepoint(position)

    def check_box_intersection(self, hitbox: pygame.Rect):
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
        if(int(hitbox.bottom) != hitbox.bottom):
            return False

        return self.check_box_intersection(hitbox) and self.check_box_intersection(hitbox.move(0, -1))
