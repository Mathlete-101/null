import os.path

import pygame

from graphics import graphics
import tools
from graphics.graphic_class.graphic import Graphic


def assemble():

    energy_parts = tools.lists.flatten2d(tools.transform.split_sheet(
        pygame.image.load(os.path.join("resources", "images", "blocks", "energy_parts.png"))
    ))

    graphics.add(Graphic(energy_parts), "energy_parts")
