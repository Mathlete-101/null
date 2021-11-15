import pygame

from level.level import Level
from tools import duple
from tools.transform import scale_factor as scale


def render(level: Level):
    scale_factor = 5
    dim = duple.scale(level.dim, 21)
    scale_dim = duple.scale(dim, scale_factor)
    level_render = pygame.Surface(scale_dim)
    level_render.fill((0, 0, 255))

    for i in range(0, level.dim[0]):
        for j in range(0, level.dim[1]):
            render_location = (i * 21 * scale_factor, j * 21 * scale_factor)

            if level.background[i][j]:
                level_render.blit(scale(level.background[i][j].render(), scale_factor), render_location)
            if level.main[i][j]:
                level_render.blit(scale(level.main[i][j].render(), scale_factor), render_location)

    level_render.blit(scale(level.player.render(), scale_factor),
                      duple.floor(duple.scale(level.player.location, scale_factor * 21)))

    print(duple.floor(duple.scale(level.player.location, scale_factor * 21)))

    for i in range(0, level.dim[0]):
        for j in range(0, level.dim[1]):
            render_location = (i * 21 * scale_factor, j * 21 * scale_factor)

            if level.foreground[i][j]:
                level_render.blit(scale(level.foreground[i][j].render(), scale_factor), render_location)

    return level_render
