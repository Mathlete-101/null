import math

import pygame

from animation.animation import Animation
from animation.groups.directional_animation_group import DirectionalAnimationGroup
from animation.loop_directional_animation import LoopDirectionalAnimation
from effect.effect import Effect
from effect.trimmed_effect import TrimmedEffect
from game_object.static.block import Block
from engine import keys
from graphics import graphics
from tools import duple


class Player(object):

    def __init__(self, level, location=(1, 1)):
        self.location = location
        self.static_animation = LoopDirectionalAnimation(graphics.get("player_static"), 6)
        self.directional_animation_group: DirectionalAnimationGroup = DirectionalAnimationGroup()
        self.directional_animation_group.add(self.static_animation)
        self.velocity = (0, 0)
        self.level = level
        self.image_offset = (-14, -22)
        self.is_supported = False
        self.refresh_support()
        self.laser_cooldown = 0
        self.last_dir_is_left = False

    @property
    def x(self):
        return self.location[0]

    @x.setter
    def x(self, val):
        self.location = (val, self.location[1])

    @property
    def y(self):
        return self.location[1]

    @y.setter
    def y(self, val):
        self.location = (self.location[0], val)

    @property
    def vx(self):
        return self.velocity[0]

    @vx.setter
    def vx(self, val):
        self.velocity = (val, self.velocity[1])

    @property
    def vy(self):
        return self.velocity[1]

    @vy.setter
    def vy(self, val):
        self.velocity = (self.velocity[0], val)

    @property
    def surrounding_blocks(self):
        return [x[math.floor(self.y) - 1:math.floor(self.y) + 3] for x in
                self.level.main[math.floor(self.x) - 1:math.floor(self.x) + 2]]

    @property
    def hitbox(self):
        return pygame.Rect(self.x * 42, self.y * 42, 14, 20)

    @property
    def speed(self):
        return math.sqrt(math.pow(self.vx, 2) + math.pow(self.vy, 2))

    @property
    def bottom(self):
        return self.y + self.hitbox.h / 42

    @bottom.setter
    def bottom(self, val):
        self.y = val - self.hitbox.h / 42

    @property
    def top(self):
        return self.y

    @top.setter
    def top(self, value):
        self.y = value

    @property
    def left(self):
        return self.x

    @left.setter
    def left(self, val):
        self.x = val

    @property
    def left_supported(self):
        return self.left == math.floor(self.left)

    @property
    def right(self):
        return self.x + self.hitbox.width / 42

    @right.setter
    def right(self, val):
        self.x = val - self.hitbox.width / 42

    @property
    def right_supported(self):
        return self.right == math.floor(self.right)

    @property
    def x_center(self):
        return self.x + self.hitbox.width / 84

    @x_center.setter
    def x_center(self, val):
        self.x = val - self.hitbox.width / 84

    @property
    def next_location(self):
        return duple.add(self.location, self.velocity)

    @property
    def next_x(self):
        return self.next_location[0]

    @property
    def next_y(self):
        return self.next_location[1]

    @property
    def next_bottom(self):
        return self.next_y + self.hitbox.h / 42

    @property
    def next_top(self):
        return self.next_y

    @property
    def next_left(self):
        return self.next_x

    @property
    def next_right(self):
        return self.next_x + self.hitbox.width / 42

    @property
    def next_hitbox(self):
        return pygame.Rect(self.next_x, self.next_y, self.hitbox.width, self.hitbox.height)

    @property
    def render_location(self):
        return duple.add(self.image_offset, duple.scale(self.location, 42))

    def refresh_support(self):
        self.is_supported = self.check_support()

    def check_support(self, offset=(0, 0)):
        supported = False
        hitbox = self.hitbox.copy()
        hitbox.x += offset[0]
        hitbox.y += offset[1]
        for row in self.surrounding_blocks:
            for block in row:
                supported = supported or block.check_support(hitbox)
                if block.check_support(hitbox):
                    # block.alert()
                    pass

        return supported

    def update(self):

        self.refresh_support()

        if not self.is_supported:
            self.vy += 0.02

        # side to side motion
        if keys.left:
            self.vx = -0.15
            self.last_dir_is_left = True
        elif keys.right:
            self.vx = 0.15
            self.last_dir_is_left = False
        else:
            self.vx = 0

        # constrain the y velocity to prevent problems
        self.vy = self.vy if self.vy < 0.99999 else 0.99999
        self.vy = self.vy if self.vy > -0.99999 else -0.99999

        corners = [self.hitbox.topleft, self.hitbox.topright, self.hitbox.bottomleft, self.hitbox.bottomright]
        corners = list(set([duple.floor(duple.scale(x, 1 / 42)) for x in corners]))
        # check to see if the space we are currently on modifies our movement somehow
        check_blocks = [self.level.main[c[0]][c[1]] for c in corners]
        for b in check_blocks:
            if b.special_collision:
                b.collide_special(self)

        if self.is_supported:
            if keys.up:
                self.vy = -0.3
            self.vy = min(self.vy, 0)

        # grid checking - these are all very similar, but with subtle but EXTREMELY IMPORTANT differences
        if self.vy > 0:
            b = self.bottom
            nb = self.next_bottom
            nx = self.x if self.left_supported else self.next_x
            if math.floor(nb) != math.floor(b):
                target = self.level.main[math.floor(nx)][math.floor(nb)]
                target2 = self.level.main[math.floor(nx) + 1][math.floor(nb)]

                # this fixes a small movement bug
                funny_correction = False
                if math.floor(self.next_x) != math.floor(self.x):
                    target3 = self.level.main[math.floor(nx)][math.floor(self.bottom)]
                    if target3.is_right_wall:
                        funny_correction = True

                if target.special_collision and not funny_correction:
                    target.init_collide_special(self)
                if target2.special_collision:
                    target2.collide_special(self)

                # i hate the movement code
                if not funny_correction:
                    if target.is_floor:
                        self.bottom = math.ceil(self.bottom)
                        self.vy = 0
                    if target2.is_floor and target2.x - self.x - .05 < self.hitbox.width / 42 and not self.level.main[math.floor(nx) + 1][math.floor(self.bottom)].is_left_wall:
                        self.bottom = math.ceil(self.bottom)
                        self.vy = 0
                        if not self.check_support(self.velocity):
                            self.x += 0.05


        elif self.vy < 0:
            t = self.top
            nt = self.next_top
            nx = self.x if self.left_supported else self.next_x
            if math.floor(nt) != math.floor(t):
                target: Block = self.level.main[math.floor(nx)][math.floor(self.next_y)]
                target2: Block = self.level.main[math.floor(nx) + 1][math.floor(self.next_y)]

                funny_correction = False
                if math.floor(self.next_x) != math.floor(self.x):
                    target3 = self.level.main[math.floor(nx)][math.floor(self.top)]
                    if target3.is_right_wall:
                        funny_correction = True

                if target.special_collision:
                    target.init_collide_special(self)
                if target2.special_collision:
                    target2.collide_special(self)
                if (
                        target.is_ceiling or target2.is_ceiling and target2.x - self.x + .01 < self.hitbox.width / 42) and not funny_correction:
                    self.top = math.floor(self.top)
                    self.vy = 0

        if self.vx < 0:
            l = self.left
            nl = self.next_left
            if math.floor(nl) != math.floor(l):
                target: Block = self.level.main[math.floor(self.next_x)][math.floor(self.next_y)]
                target2: Block = self.level.main[math.floor(self.next_x)][math.floor(self.next_y) + 1]
                if target.special_collision:
                    target.init_collide_special(self)
                if target2.special_collision:
                    target2.collide_special(self)
                if target.is_left_wall or target2.is_ceiling and target2.y - self.next_y < self.hitbox.height / 42:
                    self.left = math.floor(self.left)
                    self.vx = 0
        elif self.vx > 0:
            r = self.right
            nr = self.next_right
            if math.floor(nr) != math.floor(r) or self.right_supported:
                target: Block = self.level.main[math.floor(self.next_right)][math.floor(self.next_y)]
                target2: Block = self.level.main[math.floor(self.next_right)][math.floor(self.next_y) + 1]
                if target.special_collision:
                    target.init_collide_special(self)
                if target2.special_collision:
                    target2.collide_special(self)

                if target.is_left_wall or (target2.is_left_wall and self.next_bottom > target2.y):
                    self.right = math.floor(self.right) + (0 if self.right_supported else 1)

                    self.vx = 0

        # just constrain motion to be within the level. This shouldn't really matter
        if not 0 < self.next_x < self.level.dim[0]:
            self.vx = 0

        if not 0 < self.next_y < self.level.dim[1]:
            self.vy = 0

        # update position
        self.location = self.next_location

        # laser gun
        if keys.a and self.laser_cooldown == 0:
            direction = -1 if self.last_dir_is_left else 1
            offset = direction
            while offset + math.floor(self.x + 28 / 42) < len(self.level.main) and not \
            self.level.main[math.floor(self.x + 28 / 42 - (self.last_dir_is_left)) + offset][math.floor(self.y)].opaque:
                self.level.effects.append(
                    Effect(Animation(graphics.get("player_laser")), duple.add(self.render_location, (offset * 42, 0)),
                           True))
                offset += direction
            if self.last_dir_is_left:
                left = (math.floor((self.location[0] - math.floor(self.location[0] + 28 / 42)) * 42) + 28) % 42
                rect = pygame.Rect(42 - left, 0, left, 42)
                self.level.effects.append(TrimmedEffect(Animation(graphics.get("player_laser")),
                                                        duple.add(self.render_location, (offset * 42, 0)), rect, True))
            else:
                right = -(math.ceil((self.location[0] - math.ceil(self.location[0] + 28 / 42)) * 42) + 27) % 42
                rect = pygame.Rect(0, 0, right, 42)
                self.level.effects.append(TrimmedEffect(Animation(graphics.get("player_laser")),
                                                        duple.add(self.render_location, (offset * 42, 0)), rect, True))

            impact_block = self.level.main[math.floor(self.x + 28 / 42 - self.last_dir_is_left) + offset][
                math.floor(self.y)]
            if "energy_receptive" in impact_block.tags:
                impact_block.on_energy_hit(1)

            self.laser_cooldown = 10

        if self.laser_cooldown > 0:
            self.laser_cooldown -= 1

        self.directional_animation_group.set_left(self.last_dir_is_left)

    def render(self):
        if self.speed <= 0.001:
            render = self.static_animation.render()
            return render
        else:
            return self.static_animation.render()
