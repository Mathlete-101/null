import pygame;


def split_sheet(surface):
    imgs = []
    i = 0
    j = 0
    while j < surface.get_size()[1] - 22:
        row = []
        while i < surface.get_size()[0] - 22:
            rect = pygame.Rect(i + 1, j + 1, 20, 20)
            row.append(surface.subsurface(rect))
            i += 22
        i = 0
        j += 22
        imgs.append(row.copy())
        row = []
    return imgs


def scale_factor(surface, factor):
    return pygame.transform.scale(surface, (surface.get_size()[0] * factor, surface.get_size()[1] * factor))
