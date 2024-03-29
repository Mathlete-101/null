import math

import pygame

from game_object.static.no_sides_block import NoSidesBlock
from graphics import graphics

# Note about ladders:
# If you space ladders with two blocks in between them, you can effectively create monkey bars.
# However, there are alignment effects - some alignments cause you to move up when jumping across monkey bars,
# but some cause you to move down. I'm not fixing this. It might be fun to use this mechanic later in the game.


class Ladder(NoSidesBlock):

    def __init__(self, position, render_target):
        super().__init__(position, render_target, graphics.get("ladder").get().copy())
        self.hitbox = pygame.Rect((self.render_position[0] + 8, self.render_position[1], 26, 42))
        self.tags.append("ladder")
        self.is_top_ladder = False

    @property
    def opaque(self):
        return False

    def check_support(self, hitbox):
        return self.is_top_ladder and super().check_support(hitbox)

    @property
    def special_collision(self):
        return True

    def collide_special(self, player):
        if self.hitbox.colliderect(player.hitbox):
            player.suppress_yoyo()
            player.suppress_double_jump()
            if player.controller.ladder_up:
                player.vy = -0.1
                # This might be needed. If there are bugs with the ladder, try player.controller.ladder_up = False or maybe player.controller.ladder_down = False or maybe even player.controller.jump = False
                # if math.floor(player.next_bottom) != math.floor(player.bottom) and math.floor(player.bottom) == self.y and self.is_top_ladder:
            elif player.controller.ladder_down:
                player.vy = 0.1
            else:
                player.vy = 0


    def init_collide_special(self, player):
        self.collide_special(player)


