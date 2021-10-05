import os.path

import pygame

import tools

from graphics import graphics

from graphics.graphic_class.shuffle_graphic import ShuffleGraphic
from tools.apply import blit_all, blit_all_to, blit_to_all


def assemble():
    # premature optimization is the root of all evil, or so they say

    # load in the platforms sheet
    platforms = tools.transform.split_sheet(
        pygame.image.load(os.path.join("resources", "images", "blocks", "platforms.png")))

    # split up the sections
    background = platforms[0][0]
    decorations = platforms[1]
    foregrounds = platforms[0][1:4]
    edges = platforms[2]

    # take all of the background peices and get every possible rotation
    transformed_decorations = tools.lists.flatten2d(
        [[pygame.transform.rotate(dec.copy(), 90 * x) for dec in decorations] for x in range(4)])

    # blit them all onto the background
    backgrounds = blit_all_to(background, transformed_decorations)

    # rotate the slash thing and and add it to the foregrounds
    foregrounds.append(pygame.transform.rotate(foregrounds[0], 90))

    foreground_names = ["slash", "cross", "box", "slash_flipped"]
    edge_names = ["_one_edge", "_corner", "_three_edge", "_four_edge", "_wall"]

    # generate a shuffle graphic for every possible foreground and background combination
    for i in range(0, 4):
        name = "platform" + foreground_names[i]
        base = blit_to_all(backgrounds, foregrounds[i])

        graphics.add(ShuffleGraphic(base.copy()), name)

        for j in range(0, 4):
            added = blit_to_all(base, edges[i])
            graphics.add(blit_to_all(base, edges[i]), name + edge_names[j])
