import random

import numpy

import graphics.graphics
from blocks.block import Block
from graphics import graphics
from level.level import Level
from level.level_text import LevelText


# Key

# <space> = air
# B = a standard block/wall/whatever

def assign(level_text: LevelText):
    level = Level(level_text.dim)

    for i in range(0, level_text.dim[0]):
        for j in range(0, level_text.dim[1]):
            location = (i, j)
            chars = (level_text.background.get(location),
                     level_text.main.get(location),
                     level_text.foreground.get(location))

            if chars[1] == "B":
                surroundings = level_text.main.get_surrounding_pieces(location)
                edges = [[char != 'B' for char in row] for row in surroundings]

                print('-----------')
                print(location)
                print(numpy.array(surroundings))

                level.set(location, Block(location, graphics.get("platform_" + ("cross" if (location[0] + location[1]) % 2 else "box")).get_with_edge(edges)))

    return level
