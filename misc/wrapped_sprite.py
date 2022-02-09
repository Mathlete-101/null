import pygame.sprite
from pygame.sprite import AbstractGroup


class WrappedSprite(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, location) -> None:
        super().__init__()
        self.image = image
        self.rect = pygame.Rect(location[0], location[1], image.get_size()[0], image.get_size()[1])

    def update(self):
        pass
