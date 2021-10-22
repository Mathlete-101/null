import os.path

import pygame

import tools

from graphics import graphics
from graphics.graphic_class.shuffle_edge_graphic import ShuffleEdgeGraphic

from graphics.graphic_class.shuffle_graphic import ShuffleGraphic
from tools.apply import blit_all_to, blit_to_all


def assemble():
    # premature optimization is the root of all evil, or so they say

    # load in the platforms sheet
    platforms = tools.transform.split_sheet(
        pygame.image.load(os.path.abspath(os.path.join("resources", "images", "blocks", "platforms.png"))))

    # split up the sections
    background = platforms[0][0]
    decorations = platforms[1][0:4]
    foregrounds = platforms[0][1:4]
    edges = platforms[2]
    edge = platforms[2][0]
    corner = platforms[2][1]

    # take all of the background peices and get every possible rotation
    transformed_decorations = tools.lists.flatten2d(
        [[pygame.transform.rotate(dec.copy(), 90 * x) for dec in decorations] for x in range(4)])

    # blit them all onto the background
    backgrounds = blit_all_to(background, transformed_decorations)

    # rotate the slash thing and and add it to the foregrounds
    foregrounds.append(pygame.transform.rotate(foregrounds[1], 90))

    foreground_names = ["cross", "slash", "box", "slash_flipped"]

    # generate a shuffle graphic for every possible foreground and background combination
    for i in range(0, len(foreground_names)):
        name = "platform_" + foreground_names[i]
        base = blit_to_all(backgrounds, foregrounds[i])

        graphics.add(ShuffleEdgeGraphic(base.copy(), edge, corner, corner), name)
