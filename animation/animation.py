from pygame import Surface

from graphics.graphic_class.graphic import Graphic


class Animation(object):
    def __init__(self, graphic: Graphic, slowness=1):
        self.graphic = graphic
        self.position = 0
        self.slowness = slowness
        self.length = len(self.graphic) * self.slowness

    @property
    def dim(self):
        return self.graphic.get()[0].get_size()

    def increment(self):
        self.position += 1

    def get_frame(self, position):
        return self.graphic.get()[position]

    def render(self):
        if self.ended:
            surface = Surface(self.dim)
            surface.fill((255, 255, 255))
            surface.set_colorkey((255, 255, 255))
            return surface

        img = self.get_frame(self.position // self.slowness)
        self.increment()
        return img

    @property
    def ended(self):
        return self.length <= self.position
