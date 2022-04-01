import os

import pygame

from graphics.graphic_class.graphic import Graphic
from tools import transform
from graphics import graphics


def assemble():
    columns = transform.split_sheet(pygame.image.load(os.path.join("resources", "images", "blocks", "columns.png")))

    graphics.add(Graphic(columns[0][0]), "column")
    graphics.add(Graphic(columns[0][1]), "column_base")
