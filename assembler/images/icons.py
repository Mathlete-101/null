import pygame
import os
from graphics import graphics

import tools.transform


def assemble():
    # load all files in the directory resources/images/misc/controller_types as pygame surfaces

    for name in os.listdir(os.path.join("resources", "images", "misc", "controller_types")):
        icon = pygame.image.load(os.path.join("resources", "images", "misc", "controller_types", name))
        icon = tools.transform.scale_factor(icon, 8)
        img_name = name.split(".")[0]
        graphics.add(icon, img_name)