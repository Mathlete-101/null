import random
from typing import List

import pygame
from stopwatch import Stopwatch

import tools.transform
from graphics import graphics
from animation.animation import Animation
from effect.effect import Effect
from game_object.mobile.player import Player
from game_object.static.air import Air
from game_object.static.block import Block
from level.null_group import NullGroup
from networker.network_manager import NetworkManager
from tools import duple


def generate_blank_grid(dim):
    grid = []
    for i in range(0, dim[0]):
        row = []
        for j in range(0, dim[1]):
            row.append(Air((i * 21, j * 21)))
        grid.append(row)
    return grid

def generate_background_surface(dim):
    background = pygame.Surface(duple.scale(dim, 42))
    background_bases = graphics.get("background_base")
    background_emblems = graphics.get("background_emblem")
    for i in range(dim[0]):
        for j in range(dim[1]):
            render_location = duple.scale((i, j), 42)
            background.blit(background_bases.get(), render_location)
            if random.random() < 0.1:
                background.blit(background_emblems.get(), render_location)

    return background

class Level:
    def __init__(self, dim):
        self.render_dim = duple.scale(dim, 21 * 2)
        # self.background_surface = tools.transform.get_clear_surface(self.render_dim)
        # self.main_surface = tools.transform.get_clear_surface(self.render_dim)
        # self.foreground_surface = tools.transform.get_clear_surface(self.render_dim)
        self.background: List[List[Block]] = generate_blank_grid(dim)
        self.main = generate_blank_grid(dim)
        self.foreground = generate_blank_grid(dim)
        self.dim = dim
        self.player = Player(self)
        self.scale_factor = 2
        self.effects = []
        self.network_manager = NetworkManager(self)
        self.null_speed = 30
        self.null_timer = 0
        self.null_line = 0

        # Rendering stuff
        self.world_surface = generate_background_surface(self.dim)
        self.render_surface = pygame.Surface(self.render_dim)
        self.block_sprite_group = pygame.sprite.Group()
        self.continuous_block_sprite_group = pygame.sprite.Group()
        self.effect_sprite_group = pygame.sprite.Group()
        self.player_sprite_group = pygame.sprite.Group(self.player)
        self.active_null_sprite_groups = [NullGroup(0, self.dim[0])]
        self.active_null_sprite_groups[0].update()

        self.col_groups = [pygame.sprite.Group() for x in range(self.dim[0])]

    def initialize(self):
        self.network_manager.initialize()
        self.block_sprite_group.draw(self.world_surface)
        self.render_surface.blit(self.world_surface, (0, 0))

    def set(self, location: (int, int), block):
        self.main[location[0]][location[1]] = block

    def set_background(self, location: (int, int), block):
        self.background[location] = block

    def set_foreground(self, location: (int, int), block):
        self.foreground[location] = block

    def update(self):
        if self.player.x < self.null_line - 7:
            from engine.game import engine
            engine.end_game()
        self.player.update()
        if self.network_manager:
            self.network_manager.update()
        self.null_timer += 1
        if self.null_timer >= self.null_speed:
            self.tick_null()
            self.null_timer = 0


    def set_player_location(self, location):
        self.player.location = location

    def add_effect(self, effect):
        if effect.render_location[0] <= 42 * (self.null_line - 6):
            return
        self.effects.append(effect)
        self.effect_sprite_group.add(effect)

    def render(self):
        self.continuous_block_sprite_group.clear(self.render_surface, self.world_surface)
        self.player_sprite_group.clear(self.render_surface, self.world_surface)
        self.effect_sprite_group.clear(self.render_surface, self.world_surface)
        self.continuous_block_sprite_group.draw(self.render_surface)
        self.player_sprite_group.draw(self.render_surface)
        self.effect_sprite_group.draw(self.render_surface)
        for group in self.active_null_sprite_groups:
            group.draw(self.render_surface)
        return self.render_surface
        # self.render_base.blit(self.background_surface, (0, 0))
        # self.render_base.blit(self.main_surface, (0, 0))
        # self.render_base.blit(tools.transform.scale_factor(self.player.render(), 3), self.player.render_location)
        # next_effects = []
        # for effect in self.effects:
        #     effect.render(self.render_base)
        #     if not effect.animation.ended:
        #         next_effects.append(effect)
        # self.effects = next_effects
        #
        # return self.render_base

    def prepare_for_destruction(self):

        pass

        # This doesn't work yet
        # get rid of anything that might have a reference to this object, thus breaking all loops and allowing for
        # garbage collection
        # del self.main
        # del self.background
        # del self.foreground
        # del self.network_manager
        # del self.player

    def tick_null(self):
        self.null_line += 1
        if len(self.active_null_sprite_groups) >= 8:
            group = self.active_null_sprite_groups.pop(0)
            for sprite in list(self.col_groups[group.position].sprites()):
                sprite.kill()
            group.draw(self.render_surface)
            group.draw(self.world_surface)
            for sprite in list(group.sprites()):
                sprite.kill()

            render_line = (self.null_line - 6) * 42
            for effect in self.effects:
                if effect.render_location[0] <= render_line:
                    effect.kill()

        self.active_null_sprite_groups.append(NullGroup(self.null_line, self.dim[0]))

        for group in self.active_null_sprite_groups:
            group.update()
