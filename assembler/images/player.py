import os.path

import numpy
import pygame.image

import tools.transform
from graphics import graphics
from graphics.graphic_class.animation_graphic import AnimationGraphic
from graphics.graphic_class.graphic import Graphic


def assemble():

    static = tools.transform.split_sheet(pygame.image.load(os.path.join("resources", "images", "player", "static.png")))

    graphics.add(AnimationGraphic([[static[0][x], static[1][x]] for x in range(0, 4)]), "player_static")

    laser = tools.transform.split_sheet(pygame.image.load(os.path.join("resources", "images", "player", "laser.png")))

    graphics.add(AnimationGraphic(laser[0][0:4]), "player_laser")
