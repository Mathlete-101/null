import os.path

import pygame

import tools
from graphics import graphics
from graphics.graphic_class.edge_graphic import EdgeGraphic
from graphics.graphic_class.graphic import Graphic
from graphics.graphic_class.shuffle_edge_graphic import ShuffleEdgeGraphic
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
    # backgrounds = [background]

    # rotate the slash thing and and add it to the foregrounds
    foregrounds.append(pygame.transform.rotate(foregrounds[1], 90))

    foreground_names = ["cross", "slash", "box", "slash_flipped"]

    # generate a shuffle graphic for every possible foreground and background combination
    for i in range(0, len(foreground_names)):
        name = "platform_" + foreground_names[i]
        base = blit_to_all(backgrounds, foregrounds[i])
        alt_base = [platforms[2][2].copy()]
        alt_base[0].blit(foregrounds[i], (0, 0))

        graphics.add(ShuffleEdgeGraphic(base.copy(), edge, corner, corner), name)
        graphics.add(ShuffleEdgeGraphic([platforms[2][3].copy()], edge, corner, corner), name + "_alt")

    # crates
    graphics.add(EdgeGraphic(platforms[0][4], platforms[1][4], platforms[2][4], platforms[3][4]), "large_crate")

    # blocks laser goes through
    graphics.add(Graphic(platforms[0][5]), "platform_laser_through")

    # thin platform for aesthetic purposes
    graphics.add(Graphic(platforms[0][6]), "platform_thin")

