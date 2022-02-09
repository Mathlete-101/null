import pygame

from externals.leaderboard.leaders import Leaders
from misc.wrapped_sprite import WrappedSprite
from tools.text import render_font_cool as Text

class Leaderboard:
    def __init__(self, size):
        from engine.engine import engine
        self.size = size
        self.background_surface = pygame.Surface(size)
        self.background_surface.fill((60, 60, 80))
        self.render_surface = self.background_surface.copy()

        self.leaderboard = Leaders()
        self.info_text = pygame.sprite.Group()
        self.info_text.add(WrappedSprite(Text("Your Score:", zoom=2), (size[0] / 8, size[1] / 4)))
        self.info_text.add(WrappedSprite(Text(format(engine.score, "06"), zoom=6), (size[0] / 8, size[1] / 3)))
        self.info_text.add(WrappedSprite(Text("Leaders", zoom=3), (size[0] * 5/8, 50)))




    def update(self):
        self.leaderboard.update()

    def render(self):
        self.leaderboard.clear(self.render_surface, self.background_surface)
        self.info_text.clear(self.render_surface, self.background_surface)
        self.leaderboard.draw(self.render_surface)
        self.info_text.draw(self.render_surface)
        return self.render_surface