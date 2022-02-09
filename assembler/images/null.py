import os.path

import pygame.image

import tools.transform
import tools.lists
from graphics import graphics
from graphics.graphic_class.shuffle_graphic import ShuffleGraphic


def assemble():
    null = tools.transform.split_sheet(pygame.image.load(os.path.join("resources", "images", "blocks", "null.png")))

    null = tools.lists.flatten2d([x[0:3] for x in null[0:3]])

    null = [[pygame.transform.rotate(n.copy(), 90 * x) for n in null] for x in range(4)]

    null = tools.lists.flatten2d(null)

    graphics.add(ShuffleGraphic(null), "null")
