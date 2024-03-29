import pygame
import tools

from animation.animation import Animation


class Effect(pygame.sprite.Sprite):
    def __init__(self, animation: Animation, render_location, scale=False):
        super().__init__()
        self.animation: Animation = animation
        self.render_location = render_location
        self.scale = scale
        self.rect = pygame.Rect(render_location[0], render_location[1], 42, 42)
        self.group = pygame.sprite.Group(self)

    @property
    def image(self):
        frame = self.animation.render()
        return frame

    @property
    def ended(self):
        return self.animation.ended

    def __repr__(self):
        return f"<Effect ended?:{self.animation.ended}>"
