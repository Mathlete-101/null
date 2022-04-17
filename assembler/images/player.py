import os.path

import numpy
import pygame.image

import tools.transform
from graphics import graphics
from graphics.graphic_class.animation_graphic import AnimationGraphic
from graphics.graphic_class.graphic import Graphic
from graphics.graphic_class.shuffle_animation_graphic import ShuffleAnimationGraphic
from graphics.graphic_class.shuffle_graphic import ShuffleGraphic


def assemble():
    for i in range(0, 2):

        #standing still
        static = tools.transform.split_sheet(pygame.image.load(os.path.join("resources", "images", "player", str(i), "static.png")))

        graphics.add(AnimationGraphic([[static[0][x], static[1][x]] for x in range(0, 4)]), "player_static_" + str(i))

        #walking/jumping
        moving = tools.transform.split_sheet(pygame.image.load(os.path.join("resources", "images", "player", str(i), "moving.png")))

        graphics.add(AnimationGraphic([[moving[0][x], moving[1][x]] for x in range(0, 4)]), "player_walking_" + str(i))
        graphics.add(AnimationGraphic([[moving[2][0], moving[2][1]]]), "player_jumping_" + str(i))

        #laser
        laser = tools.transform.split_sheet(pygame.image.load(os.path.join("resources", "images", "player", str(i), "laser.png")))
        images = []
        for j in range(0, 4):
            img = tools.transform.get_clear_surface((84, 42))
            img.blit(laser[0][j], (0, 0))
            img.blit(laser[0][j], (42, 0))
            images.append(img)

        graphics.add(AnimationGraphic(laser[0][0:4]), "player_laser_" + str(i))
        graphics.add(AnimationGraphic(laser[0][0:4]), "player_laser_impact_" + str(i))
        graphics.add(AnimationGraphic(images), "player_laser_long_" + str(i))

        # movement belt
        m_belt = tools.transform.split_sheet(pygame.image.load(os.path.join("resources", "images", "player", "movement_belt.png")))

        # double jump animation
        graphics.add(AnimationGraphic(m_belt[0][0:6]), "player_double_jump")

        # dash animation things
        graphics.add(ShuffleAnimationGraphic(m_belt[1][0:8]), "player_dash")

        # yoyo animations
        graphics.add(AnimationGraphic(m_belt[3][0:15]), "player_yoyo_portal")
        graphics.add(AnimationGraphic(m_belt[4][0:5]), "player_yoyo_teleport")
        graphics.add(AnimationGraphic(m_belt[5][0:5]), "player_yoyo_portal_end")

        # level builder player
        level_builder_player = tools.transform.split_sheet(pygame.image.load(os.path.join("resources", "images", "player", "level_builder_player.png")))

        graphics.add(Graphic(level_builder_player[0][0]), "level_builder_player")
        graphics.add(Graphic(level_builder_player[0][1]), "level_builder_player_background")

