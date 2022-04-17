import pygame

from assembler.levels import levels
from assigner import assigner
from controller.full_keyboard_controller import FullKeyboardController
from graphics import graphics
from level.level_text import LevelText
from tools import duple

class LevelBuilderPlayer(pygame.sprite.Sprite):
    class Mode:
        MAIN = 0
        BACKGROUND = 1

    def __init__(self, level, level_text, meta_data, level_name):
        super().__init__()
        self.main_image = graphics.get("level_builder_player").get()
        self.background_image = graphics.get("level_builder_player_background").get()
        self.controller = FullKeyboardController()
        self.position = (0, 0)
        self.level_text: LevelText = level_text
        self.level = level
        self.meta_data = meta_data
        self.level_name = level_name
        self.mode = self.Mode.MAIN
        self.save_counter = 20
        self.initialized = False

    def update(self):
        if not self.initialized:
            self.initialized = True
            from engine.game import engine
            if engine.level_builder_player_location is not None:
                self.location = engine.level_builder_player_location

        # movement
        if self.controller.get_key(pygame.K_LEFT):
            self.position = (self.position[0] - 1, self.position[1])
        elif self.controller.get_key(pygame.K_RIGHT):
            self.position = (self.position[0] + 1, self.position[1])
        elif self.controller.get_key(pygame.K_UP):
            self.position = (self.position[0], self.position[1] - 1)
        elif self.controller.get_key(pygame.K_DOWN):
            self.position = (self.position[0], self.position[1] + 1)

        # player control testing
        if self.controller.get_key(pygame.K_RETURN):
            block = self.level.main[self.x][self.y]
            if "energy_receptive" in block.tags:
                block.on_energy_hit(1)

        # save and reload
        elif self.controller.get_key(pygame.K_s, ctrl=True):
            self.save_level()
        elif self.controller.get_key(pygame.K_w, ctrl=True):
            self.save_level()
            self.level.initialize()
        elif self.controller.get_key(pygame.K_r, ctrl=True):
            self.save_level()
            from engine.game import engine
            engine.current_level_number = 0
            engine.level_builder_player_location = self.position
            engine.next_level()

        # change modes
        elif self.controller.get_key(pygame.K_TAB):
            if self.mode == self.Mode.MAIN:
                self.mode = self.Mode.BACKGROUND
            elif self.mode == self.Mode.BACKGROUND:
                self.mode = self.Mode.MAIN

        # place
        else:
            if self.controller.last_key_pressed != '':
                self.set(self.controller.last_key_pressed, self.current_layer)
                self.save_counter -= 1

        # save periodically
        if self.save_counter <= 0:
            self.save_level()
            self.save_counter = 20

    def save_level(self):
        levels.save_level(self.level_text, "level_builder", self.level_name)

    def set(self, char, layer):
        layer.text[self.x][self.y] = char
        assigner.assign_individual(self.position, self.level, self.level_text, self.meta_data, self.level_name)
        self.level.draw_level()

    @property
    def image(self):
        if self.mode == self.Mode.MAIN:
            return self.main_image
        elif self.mode == self.Mode.BACKGROUND:
            return self.background_image

    @property
    def current_layer(self):
        if self.mode == self.Mode.MAIN:
            return self.level_text.main
        elif self.mode == self.Mode.BACKGROUND:
            return self.level_text.background

    # All the stuff other stuff refers to when it asks for a player that we have to have so the code will work

    @property
    def render_location(self):
        return duple.scale(self.position, 42)

    @property
    def rect(self):
        return (self.render_location[0], self.render_location[1], 42, 42)

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    @property
    def location(self):
        return self.position

    @location.setter
    def location(self, value):
        self.position = value


