import pygame
import tools

from animation.animation import Animation


class Effect:
    def __init__(self, animation: Animation, render_location, scale=False):
        self.animation: Animation = animation
        self.render_location = render_location
        self.scale = scale

    def get_frame(self):
        frame = self.animation.render()
        return tools.transform.scale_factor(frame, 2) if self.scale else frame

    def render(self, r_surface: pygame.Surface):
        r_surface.blit(self.get_frame(), self.render_location)

    def __repr__(self):
        return f"<Effect ended?:{self.animation.ended}>"
