import pygame


def blit_to_all(backgrounds, foreground, loc=(0, 0)):
    n = []
    for b in backgrounds:
        n.push(cblit(b, foreground), loc)
    return n


def blit_all_to(background, foregrounds, loc=(0, 0)):
    n = []
    for f in foregrounds:
        n.push(cblit(background, f, loc))
    return n


def cblit(background: pygame.Surface, foreground: pygame.Surface, loc=(0, 0)):
    n = background.copy()
    n.blit(foreground, loc)
    return n
