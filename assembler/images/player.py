import os.path

import numpy
import pygame.image

import tools.transform
from graphics import graphics
from graphics.graphic_class.animation_graphic import AnimationGraphic
from graphics.graphic_class.graphic import Graphic


def assemble():

    #standing still
    static = tools.transform.split_sheet(pygame.image.load(os.path.join("resources", "images", "player", "static.png")))

    graphics.add(AnimationGraphic([[static[0][x], static[1][x]] for x in range(0, 4)]), "player_static")

    #walking/jumping
    moving = tools.transform.split_sheet(pygame.image.load(os.path.join("resources", "images", "player", "moving.png")))

    graphics.add(AnimationGraphic([[moving[0][x], moving[1][x]] for x in range(0, 4)]), "player_walking")
    graphics.add(AnimationGraphic([[moving[2][0], moving[2][1]]]), "player_jumping")

    #laser
    laser = tools.transform.split_sheet(pygame.image.load(os.path.join("resources", "images", "player", "laser.png")))
    images = []
    for i in range(0, 4):
        img = tools.transform.get_clear_surface((84, 42))
        img.blit(laser[0][i], (0, 0))
        img.blit(laser[0][i], (42, 0))
        images.append(img)

    graphics.add(AnimationGraphic(laser[0][0:4]), "player_laser")
    graphics.add(AnimationGraphic(images), "player_laser_long")
