import math

import pygame

from animation.animation import Animation
from animation.groups.directional_animation_group import DirectionalAnimationGroup
from animation.loop_animation import LoopAnimation
from animation.loop_directional_animation import LoopDirectionalAnimation
from effect.effect import Effect
from effect.trimmed_effect import TrimmedEffect
from game_object.static.block import Block
from engine import keys
from graphics import graphics
from tools import duple
from tools.transform import MicroRect


class PlayerMovementOverrideCommand:
    def __init__(self, function, duration):
        self.function = function
        self.duration = duration
        self.time = 0

    def run(self, player):
        self.time += 1
        self.function(player)
        if self.time >= self.duration:
            self.time = 0
            return True
        return False

class PlayerMovementOverride:
    def __init__(self, commands):
        self.commands = commands
        self.current_command = 0

    def run(self, player):
        if self.commands[self.current_command].run(player):
            self.current_command += 1
            if self.current_command >= len(self.commands):
                self.current_command = 0
                return True
        return False





class Player(pygame.sprite.Sprite):

    def __init__(self, level, location=(1, 1)):
        super().__init__()
        self.location = location

        # animations
        self.static_animation = LoopDirectionalAnimation(graphics.get("player_static"), 6)
        self.walking_animation = LoopDirectionalAnimation(graphics.get("player_walking"), 2)
        self.jumping_animation = LoopDirectionalAnimation(graphics.get("player_jumping"), 10)

        # animation group
        self.directional_animation_group: DirectionalAnimationGroup = DirectionalAnimationGroup()
        self.directional_animation_group.add(self.static_animation)
        self.directional_animation_group.add(self.walking_animation)
        self.directional_animation_group.add(self.jumping_animation)

        self.velocity = (0, 0)
        self.level = level
        self.image_offset = (-7, -10)

        # Variables/constants for the movement belt
        self.movement_belt = False # or True
        self.movement_belt_charges = 3
        self.max_movement_belt_charges = 3
        self.override_command = None
        self.double_jump_cooldown = 0
        self.double_jump_cooldown_max = 10
        self.double_jump_suppression = 0
        self.dash_speed = 0.5
        self.yoyo_location = None
        self.yoyo_delay = 0
        self.yoyo_delay_max = 120
        self.yoyo_suppression = 0
        self.yoyo_effect = None

        def dash_left(player):
            player.vx = 0 - player.dash_speed
            player.vy = 0
            player.level.add_effect(Effect(Animation(graphics.get("player_dash"), 5), player.render_location))
        self.dash_left_command = PlayerMovementOverride([PlayerMovementOverrideCommand(dash_left, 10)])

        def dash_right(player):
            player.vx = player.dash_speed
            player.vy = 0
            player.level.add_effect(Effect(Animation(graphics.get("player_dash"), 5), player.render_location))
        self.dash_right_command = PlayerMovementOverride([PlayerMovementOverrideCommand(dash_right, 10)])

        def yoyo(player: Player):
            player.vx = 0
            player.vy = 0
            player.level.add_effect(Effect(Animation(graphics.get("player_yoyo_teleport"), 3), player.render_location))
            player.location = player.yoyo_location
            # player.level.add_effect(Effect(Animation(graphics.get("player_yoyo_teleport"), 3), player.render_location))
            player.level.add_effect(Effect(Animation(graphics.get("player_yoyo_portal_end"), 3), player.render_location))
            player.yoyo_effect.kill()
            player.yoyo_effect = None
        self.yoyo_command = PlayerMovementOverride([PlayerMovementOverrideCommand(yoyo, 1)])

        # okay, so this needs some explaining
        # I wrote some code that controls the laser, but it was tuned for a different hitbox size
        # The hitbox is separated from the image by this image offset thing
        # And this was the original one.
        # When I started changing the player, I couldn't get the laser to work right again
        # So I just took this value, passed it through its original method chain, and made the laser totally independent
        # of the hitbox. Hence, this tuple.
        self.laser_image_offset = (-14, -10)
        self.laser_diff = duple.subtract(self.laser_image_offset, self.image_offset)
        self.small_laser_diff = duple.scale(self.laser_diff, 1/42)
        self.laser_recharge_time = 20

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
        return pygame.Rect(self.x * 42, round(self.y * 42), 28, 32)

    @property
    def rect(self):
        """This determines where to draw and erase the player"""
        return pygame.Rect(self.render_location[0], self.render_location[1], 0, self.hitbox.h)

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
    def y_center(self):
        return self.y + self.hitbox.height / 84

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
        """DON'T USE, THIS IS BROKEN"""
        return pygame.Rect(self.next_x, self.next_y, self.hitbox.width, self.hitbox.height)

    @property
    def render_location(self):
        return duple.d_round(duple.add(self.image_offset, duple.scale(self.location, 42)))

    @property
    def laser_render_location(self):
        """Used for calculation of laser animations"""
        return duple.d_round(duple.add(self.laser_image_offset, duple.scale(self.location, 42)))

    @property
    def is_yoyo_active(self):
        return self.yoyo_delay > 0

    @property
    def yoyo_suppressed(self):
        return self.yoyo_suppression > 0

    @property
    def double_jump_suppressed(self):
        return self.double_jump_suppression > 0

    def refresh_support(self):
        self.is_supported = self.check_support()

    def set_override_command(self, override_commmand):
        self.override_command = override_commmand

    def suppress_yoyo(self):
        self.yoyo_suppression = 10

    def suppress_double_jump(self):
        self.double_jump_suppression = 10

    def check_support(self, offset=(0, 0)):
        supported = False
        hitbox = self.hitbox
        hitbox.x += offset[0]
        hitbox.y += offset[1]
        for row in self.surrounding_blocks:
            for block in row:
                supported = supported or block.check_support(hitbox)
                # if block.check_support(hitbox):
                #     pass

        return supported

    # don't look in here. Down this path madness lies
    def update(self):

        self.refresh_support()

        # Check for override command
        if self.override_command is not None:
            if self.override_command.run(self):
                self.override_command = None
        else:
            # Normal movement

            # Gravity
            if not self.is_supported:
                self.vy += 0.02

            # Horizontal movement
            if keys.left:
                self.vx = -0.15
                self.last_dir_is_left = True
            elif keys.right:
                self.vx = 0.15
                self.last_dir_is_left = False
            else:
                self.vx = 0

            if self.movement_belt and self.movement_belt_charges > 0:
                # Movement Belt dash
                if keys.left_double_click:
                    self.last_dir_is_left = True
                    self.override_command = self.dash_left_command
                    self.movement_belt_charges -= 1
                elif keys.right_double_click:
                    self.last_dir_is_left = False
                    self.override_command = self.dash_right_command
                    self.movement_belt_charges -= 1

                # Movement Belt yoyo trigger
                if self.movement_belt and keys.down_down and not self.yoyo_suppressed and not self.is_yoyo_active:
                    self.yoyo_location = self.location
                    self.yoyo_delay = self.yoyo_delay_max
                    self.yoyo_effect = Effect(LoopAnimation(graphics.get("player_yoyo_portal"), 2), self.render_location, self.level)
                    self.level.add_effect(self.yoyo_effect)
                    self.movement_belt_charges -= 1

            # Jumping
            if keys.a and self.is_supported:
                self.vy = -0.3
                self.double_jump_cooldown = self.double_jump_cooldown_max

            # Double jumping with movement belt
            elif keys.a_down and self.movement_belt and self.movement_belt_charges > 0 and self.double_jump_cooldown == 0 and not self.double_jump_suppressed:
                self.vy = -0.3
                self.movement_belt_charges -= 1
                self.double_jump_cooldown = self.double_jump_cooldown_max
                self.level.add_effect(Effect(Animation(graphics.get("player_double_jump"), 2), duple.add(self.render_location, (0, self.hitbox.h)), self.level))

        # Double jump cooldown
        if self.double_jump_cooldown > 0:
            self.double_jump_cooldown -= 1

        # Yoyo delay + activation
        if self.yoyo_delay > 0:
            self.yoyo_delay -= 1
            if self.yoyo_delay == 0:
                self.override_command = self.yoyo_command

        # Yoyo suppression
        if self.yoyo_suppression > 0:
            self.yoyo_suppression -= 1

        # Double jump suppression
        if self.double_jump_suppression > 0:
            self.double_jump_suppression -= 1

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
            if keys.a:
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
                    if target2.is_floor and target2.x - self.x - .01 < self.hitbox.width / 42 and not self.level.main[math.floor(nx) + 1][math.floor(self.bottom)].is_left_wall:
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

                if target.is_right_wall or target2.is_right_wall and target2.y - self.next_y < self.hitbox.height / 42:
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
                    # print(self.next_bottom, self.next_right, self.vy, self.is_supported)
                    self.vx = 0

        # just constrain motion to be within the level. This shouldn't really matter
        if not 0 < self.next_x < self.level.dim[0]:
            self.vx = 0

        if not 0 < self.next_y < self.level.dim[1]:
            self.vy = 0

        # update position
        self.location = self.next_location

        # doors
        if keys.b and "door" in self.level.main[math.floor(self.x)][math.floor(self.y)].tags:
            self.level.main[math.floor(self.x)][math.floor(self.y)].enter()
            return

        # laser gun
        if keys.b and self.laser_cooldown == 0:
            # Figure out direction
            direction = -1 if self.last_dir_is_left else 1
            offset = direction
            # Check if they are right next to a block
            if not self.level.main[math.floor(self.x_center + direction)][math.floor(self.y)].opaque:
                # Generate the main set of lasers (don't touch)
                while offset + math.floor(self.x + 28 / 42) < len(self.level.main) and not \
                self.level.main[math.floor(self.x + 28 / 42 - (self.last_dir_is_left)) + offset][math.floor(self.y)].opaque:
                    self.level.add_effect(
                        Effect(Animation(graphics.get("player_laser")), duple.add(self.laser_render_location, (offset * 42, 0)),
                               True))
                    offset += direction

                # There is a bit of magic number stuff going on here, but I can't deal with it.

                # Generate the first and last lasers if you are going left
                if self.last_dir_is_left:
                    left = (math.floor((self.location[0] - math.floor(self.location[0] + 28 / 42)) * 42) + 28) % 42
                    rect = pygame.Rect(42 - left, 0, left, 42)
                    self.level.add_effect(TrimmedEffect(Animation(graphics.get("player_laser")),
                                                            duple.add(self.laser_render_location, (offset * 42, 0)), rect, True))
                    self.level.add_effect(TrimmedEffect(Animation(graphics.get("player_laser")),
                                                            self.laser_render_location, pygame.Rect(0, 0, 14, 42), True))

                # Generate the first and last lasers if you are going right
                else:
                    right = -(math.ceil((self.location[0] - math.ceil(self.location[0] + 28 / 42)) * 42) + 27) % 42
                    rect = pygame.Rect(0, 0, right, 42)
                    self.level.add_effect(TrimmedEffect(Animation(graphics.get("player_laser")),
                                                            duple.add(self.laser_render_location, (offset * 42, 0)), rect, True))

                # Trigger whatever block you hit
                impact_block = self.level.main[math.floor(self.x + 28 / 42 - self.last_dir_is_left) + offset][
                    math.floor(self.y)]
                # Fix a bug with the lasers
                render_position_before_impact_block = ((math.floor(self.x + 28 / 42 - self.last_dir_is_left) + offset - direction) * 42,
                    self.laser_render_location[1])
                self.level.add_effect(Effect(Animation(graphics.get("player_laser_impact")), render_position_before_impact_block, True))

                if "energy_receptive" in impact_block.tags:
                    impact_block.on_energy_hit(1)
            else:
                impact_block = self.level.main[math.floor(self.x_center + direction)][math.floor(self.y)]
                if not self.last_dir_is_left:
                    self.level.add_effect(TrimmedEffect(Animation(graphics.get("player_laser_long")), duple.add(self.laser_render_location, (42, 0)), pygame.Rect(0, 0, round((impact_block.location[0] * 42 - self.laser_render_location[0] - 42)), 42), True))
                else:
                    laser_length = round((self.laser_render_location[0] - impact_block.location[0] * 42) - 29)
                    self.level.add_effect(TrimmedEffect(Animation(graphics.get("player_laser_long")), duple.add(self.laser_render_location, (-29, 0)), pygame.Rect(42 - laser_length, 0, laser_length, 42), True))
                if "energy_receptive" in impact_block.tags:
                    impact_block.on_energy_hit(1)

        # Handle the cooldown on the laser
            self.laser_cooldown = self.laser_recharge_time

        if self.laser_cooldown > 0:
            self.laser_cooldown -= 1

        # Collect collectibles
        block = self.level.main[math.floor(self.x_center)][math.floor(self.y_center)]
        if "collectible" in block.tags:
            block.collect()

        self.directional_animation_group.set_left(self.last_dir_is_left)

    @property
    def image(self):
        if self.speed <= 0.0001 and self.is_supported:
            render = self.static_animation.render()
            return render
        else:
            if self.is_supported:
                render = self.walking_animation.render()
                return render
            else:
                return self.jumping_animation.render()

        # return self.static_animation.render()
