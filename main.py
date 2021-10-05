import os
import pygame
from pygame.locals import *

import tools.transform

from assembler.assembler import assembler
from graphics import graphics

if not pygame.font: print('Warning: fonts disabled')
if not pygame.mixer: print('Warning: sounds disabled')


def main():
    pygame.init()
    screen = pygame.display.set_mode((300, 300))
    pygame.display.set_caption('hello world')

    img_file = pygame.image.load(os.path.join('resources', 'images', 'blocks', 'energy_parts.png'))
    img_file.set_colorkey((255, 255, 255))

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((155, 155, 155))

    assembler.assemble();

    # subparts = transform.split_sheet(img_file)

    background.blit(tools.transform.scale_factor(graphics.get("platform_slash"), 5))

    # font = pygame.font.Font(None, 36)
    # text = font.render("Hello world", 1, (10, 10, 10))
    # text_pos = text.get_rect()
    # text_pos.centerx = background.get_rect().centerx
    # background.blit(text, text_pos)



    screen.blit(background, (0, 0))
    pygame.display.flip()

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        screen.blit(background, (0, 0))
        pygame.display.flip()


if __name__ == '__main__': main()
