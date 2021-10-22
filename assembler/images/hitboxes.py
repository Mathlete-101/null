import os.path

import pygame.image

import tools.transform

from graphics import graphics
# from graphics.graphic_class.hitbox import Hitbox


def assemble():
    hitboxes_img = pygame.image.load(os.path.join("resources", "images", "hitboxes.png"))

    hitboxes = tools.transform.split_sheet(hitboxes_img)

    # graphics.add(Hitbox(hitboxes[0]), "hitbox_full_block")