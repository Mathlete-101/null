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


def scale_factor(surface: pygame.Surface, factor):
    new_surface = pygame.transform.scale(surface, (surface.get_size()[0] * factor, surface.get_size()[1] * factor))
    new_surface.set_colorkey(surface.get_colorkey())
    return new_surface


def get_clear_surface(dim):
    surface = pygame.Surface(dim)
    surface.fill(pygame.Color(255, 255, 255))
    surface.set_colorkey((255, 255, 255))
    return surface


def blit_rect(surface: pygame.Surface, rect, color):
    surface.fill(color, rect)
