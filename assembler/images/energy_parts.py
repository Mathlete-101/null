import os.path

import pygame

from graphics import graphics
import tools
from graphics.graphic_class.graphic import Graphic
from graphics.graphic_class.reflection_graphic import ReflectionGraphic


def assemble():
    energy_parts = (tools.transform.split_sheet(
        pygame.image.load(os.path.join("resources", "images", "blocks", "energy_parts.png"))
    ))

    graphics.add(Graphic(energy_parts[1][0]), "receiver_inactive")
    graphics.add(Graphic(energy_parts[2][0]), "receiver_active")

    graphics.add(Graphic(energy_parts[1][0]), "energy_pipe_through")
    graphics.add(ReflectionGraphic(energy_parts[1][0]), "energy_pipe_turn_right")
    graphics.add(ReflectionGraphic(energy_parts[1][0]), "energy_pipe_t_junction")
    graphics.add(Graphic(energy_parts[1][0]), "energy_pipe_cross_junction")
