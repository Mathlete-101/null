import pygame

from assembler import assembler
from engine.engine import engine
from tools.transform import MicroRect

if not pygame.font: print('Warning: fonts disabled')
if not pygame.mixer: print('Warning: sounds disabled')


def main():
    assembler.assemble()
    engine.start()

    # pygame.init()
    # screen = pygame.display.set_mode((300, 300))
    #
    # background = pygame.Surface(screen.get_size())
    # background = background.convert()
    # background.fill((155, 155, 155))
    #
    # assembler.assemble();
    #
    # # subparts = transform.split_sheet(img_file)
    #
    # background.blit(tools.transform.scale_factor(graphics.get("platform_slash_one_edge").get(), 5), (0, 0))
    #
    # # font = pygame.font.Font(None, 36)
    # # text = font.render("Hello world", 1, (10, 10, 10))
    # # text_pos = text.get_rect()
    # # text_pos.centerx = background.get_rect().centerx
    # # background.blit(text, text_pos)
    #
    #
    #
    # screen.blit(background, (0, 0))
    # pygame.display.flip()
    #
    # while 1:
    #
    #
    #     screen.blit(background, (0, 0))
    #     pygame.display.flip()


if __name__ == '__main__': main()
