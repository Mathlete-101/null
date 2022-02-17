import os.path

import pygame.image

import tools.transform
import tools.lists
from graphics import graphics
from graphics.graphic_class.reflection_graphic import ReflectionGraphic
from graphics.graphic_class.shuffle_graphic import ShuffleGraphic


def assemble():
    all_background = tools.transform.split_sheet(pygame.image.load(os.path.join("resources", "images", "misc", "background.png")))

    background = tools.lists.flatten2d([x[0:4] for x in all_background[2:4]])

    emblem = tools.lists.flatten2d([x[0:4] for x in all_background[0:2]])

    background = tools.transform.combinate(background)
    emblem = tools.transform.combinate(emblem)

    graphics.add(ShuffleGraphic(background), "background_base")
    graphics.add(ShuffleGraphic(emblem), "background_emblem")

    graphics.add(ReflectionGraphic(all_background[0][4]), "inner_wall")

    darker = pygame.Surface((42, 42))
    darker.fill(pygame.Color(0, 0, 0))
    darker.set_alpha(150)
    darker.convert_alpha()
    darker_inner_wall = all_background[0][4].copy()
    darker_inner_wall.blit(darker, (0, 0))

    graphics.add(ReflectionGraphic(darker_inner_wall), "inner_wall_dark")
