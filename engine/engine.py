import pygame

from assembler.levels.levels import levels
from blocks.block import Block
from renderer import renderer
from graphics import graphics

def start():
    pygame.init()
    screen = pygame.display.set_mode((1000, 720))

    clock = pygame.time.Clock()

    test_block = Block((0, 0), graphics.get("platform_box").get())

    while True:
        pygame.display.flip()
        screen.blit(renderer.render(levels["1"]), (0, 0))
        # screen.blit(test_block.render(), (0, 0))
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

