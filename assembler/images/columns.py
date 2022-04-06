import os

import pygame

from graphics.graphic_class.graphic import Graphic
from tools import transform
from graphics import graphics


def assemble():
    columns = transform.split_sheet(pygame.image.load(os.path.join("resources", "images", "blocks", "columns.png")))

    graphics.add(Graphic(columns[0][0]), "column")
    graphics.add(Graphic(columns[0][1]), "column_base")
    graphics.add(Graphic(columns[0][0]), "column_blue")
    graphics.add(Graphic(columns[0][1]), "column_base_blue")
    graphics.add(Graphic(columns[1][0]), "column_light")
    graphics.add(Graphic(columns[1][1]), "column_base_light")
    graphics.add(Graphic(columns[2][0]), "column_dark")
    graphics.add(Graphic(columns[2][1]), "column_base_dark")
