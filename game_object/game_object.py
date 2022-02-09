import pygame.sprite


class GameObject(pygame.sprite.Sprite):
    def __init__(self, location: (int, int)):
        super().__init__()
        self.location = location
        self.tags = []
        self.group = pygame.sprite.Group([self])

    @property
    def x(self):
        return self.location[0]

    @x.setter
    def x(self, val):
        self.location = (val, self.location[1])

    @property
    def y(self):
        return self.location[1]

    @y.setter
    def y(self, val):
        self.location = (self.location[0], val)

    def initialize(self):
        pass
