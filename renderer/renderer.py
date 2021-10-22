import pygame

import tools.transform
from level.level import Level


def render(level: Level):
    dim = (level.dim[0] * 21, level.dim[1] * 21)
    level_render = pygame.Surface((dim[0], dim[1]))
    level_render.fill((0, 0, 255))

    for i in range(0, level.dim[0]):
        for j in range(0, level.dim[1]):
            render_location = (i * 21, j * 21)

            if level.background[i][j]:
                level_render.blit(level.background[i][j].render(), render_location)
            if level.main[i][j]:
                level_render.blit(level.main[i][j].render(), render_location)
            if level.foreground[i][j]:
                level_render.blit(level.foreground[i][j].render(), render_location)

    return tools.transform.scale_factor(level_render, 2)
