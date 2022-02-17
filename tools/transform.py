import pygame;

import tools.lists


def split_sheet(surface, colorkey=(255, 255, 255), scale=True):
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
        row = [scale_factor(img, 2) for img in row]
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


def get_white_surface(dim):
    surface = pygame.Surface(dim)
    surface.fill(pygame.Color(255, 255, 255))
    # surface.set_colorkey((255, 255, 255))
    return surface


def blit_rect(surface: pygame.Surface, rect, color):
    surface.fill(color, rect)


def cp_section(surface, rect):
    s = get_clear_surface((42, 42))
    s.blit(surface.subsurface(rect), (rect[0], rect[1]))
    return s


class MicroRect:
    """A portion of the pygame.Rect class that supports float values for rectangles"""
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y + self.h

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.w

    def move(self, x, y):
        """Moves this MicroRect, then returns itself"""
        self.x += x
        self.y += y
        return self

    def intersect(self, other):
        """Calculates if this MicroRect intersects another one."""
        return rect_intersect(self, other)


def rect_intersect(a: MicroRect, b: MicroRect):
    """Calculates if two MicroRects Intersect"""
    return not (a.right < b.left or a.left > b.right or a.top > b.bottom or a.bottom < b.top)


def combinate(surfaces):
    """Takes in an array of surfaces and returns an array containing all of the possible rotations of all of those
    surfaces """
    return tools.lists.flatten2d([[pygame.transform.rotate(s.copy(), 90 * x) for s in surfaces] for x in range(4)])
