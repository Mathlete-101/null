import os

import pygame.image

from graphics import graphics
import tools.transform
from graphics.graphic_class.graphic import Graphic


def assemble():
    ladder = tools.transform.split_sheet(pygame.image.load(os.path.join("resources", "images", "blocks", "ladder.png")))

    graphics.add(Graphic(ladder[0][0]), "ladder")
    graphics.add(Graphic(ladder[0][1]), "ladder_top")
    graphics.add(Graphic(ladder[0][2]), "ladder_platform")
