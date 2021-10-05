import pygame;


def split_sheet(surface, colorkey=(255, 255, 255)):
    imgs = []
    i = 0
    j = 0
    while j < surface.get_size()[1] - 22:
        row = []
        while i < surface.get_size()[0] - 22:
            rect = pygame.Rect(i + 1, j + 1, 21, 21)
            row.append(surface.subsurface(rect))
            i += 22
        i = 0
        j += 22
        for s in row:
            s.set_colorkey(colorkey)
        imgs.append(row.copy())
        row = []
    return imgs


def scale_factor(surface, factor):
    return pygame.transform.scale(surface, (surface.get_size()[0] * factor, surface.get_size()[1] * factor))
