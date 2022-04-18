import pygame

from misc.wrapped_sprite import WrappedSprite
from tools.duple import ScreenPosition
from tools.text import render_font_cool as Text


class RecordingComplete:
    def __init__(self, dim, controller):
        self.dim = dim
        self.controller = controller
        self.controller.clear()

        self.background_surface = pygame.Surface(dim)
        self.background_surface.fill((60, 60, 80))
        self.render_surface = self.background_surface.copy()
        self.sp = ScreenPosition(self.dim)

        self.group = pygame.sprite.Group()

        self.text_line_1 = WrappedSprite(Text("Recording complete.", zoom=3), self.sp((0.1, 0.4)))
        self.text_line_2 = WrappedSprite(Text("Press the start key or A to continue.", zoom=3), self.sp((0.1, 0.6)))

        self.group.add(self.text_line_1)
        self.group.add(self.text_line_2)

    def update(self):
        if self.controller.start_enter:
            from engine.game import engine
            engine.restart()

    def render(self):
        self.group.clear(self.render_surface, self.background_surface)
        self.group.draw(self.render_surface)
        return self.render_surface


