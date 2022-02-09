import pygame.sprite

from game_object.static.block import Block


# I don't know if this works
class DirtyBlock(Block, pygame.sprite.DirtySprite):
    pass
