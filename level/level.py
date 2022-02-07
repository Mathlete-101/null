from typing import List

import pygame
from stopwatch import Stopwatch

import graphics.graphics
import tools.transform
from animation.animation import Animation
from effect.effect import Effect
from game_object.mobile.player import Player
from game_object.static.air import Air
from game_object.static.block import Block
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

class Level:
    def __init__(self, dim):
        self.render_dim = duple.scale(dim, 21 * 2)
        self.background_surface = tools.transform.get_clear_surface(self.render_dim)
        self.main_surface = tools.transform.get_clear_surface(self.render_dim)
        self.foreground_surface = tools.transform.get_clear_surface(self.render_dim)
        self.background: List[List[Block]] = generate_blank_grid(dim)
        self.main = generate_blank_grid(dim)
        self.foreground = generate_blank_grid(dim)
        self.dim = dim
        self.player = Player(self)
        self.scale_factor = 2
        self.effects = []
        self.network_manager = NetworkManager(self)
        self.render_base = pygame.Surface(self.render_dim)
        self.render_base.fill((0, 0, 255))

    def set(self, location: (int, int), block):
        self.main[location[0]][location[1]] = block

    def set_background(self, location: (int, int), block):
        self.background[location] = block

    def set_foreground(self, location: (int, int), block):
        self.foreground[location] = block

    def update(self):
        self.player.update()
        self.network_manager.update()

    def set_player_location(self, location):
        self.player.location = location

    def render(self):
        self.render_base.blit(self.background_surface, (0, 0))
        self.render_base.blit(self.main_surface, (0, 0))
        self.render_base.blit(tools.transform.scale_factor(self.player.render(), 2), self.player.render_location)
        next_effects = []
        for effect in self.effects:
            effect.render(self.render_base)
            if not effect.animation.ended:
                next_effects.append(effect)
        self.effects = next_effects

        return self.render_base
