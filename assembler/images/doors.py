import os

import pygame.image

from graphics import graphics
from graphics.graphic_class.graphic import Graphic
from tools import transform


def assemble():
    doors = transform.split_sheet(pygame.image.load(os.path.join("resources", "images", "blocks", "doors.png")))

    for i in range(0, 3):
        graphics.add(Graphic(doors[0][i]), "door_" + str(i+1))

    graphics.add(Graphic(doors[1][0]), "door_exit")