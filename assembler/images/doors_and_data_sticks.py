import os

import pygame.image

from graphics import graphics
from graphics.graphic_class.graphic import Graphic
from tools import transform


def assemble():
    doors_and_data_sticks = transform.split_sheet(pygame.image.load(os.path.join("resources", "images", "blocks", "doors_and_data_sticks.png")))

    for i in range(0, 20):
        graphics.add(Graphic(doors_and_data_sticks[0][i]), "door_" + str(i+1))

    graphics.add(Graphic(doors_and_data_sticks[1][0]), "door_exit")

    for i in range(0, 3):
        graphics.add(Graphic(doors_and_data_sticks[2][i]), "data_stick_" + str(i + 1))

    graphics.add(Graphic(doors_and_data_sticks[3][0]), "movement_belt")
