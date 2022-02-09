import pygame
import tools

from animation.animation import Animation
from effect.effect import Effect


class TrimmedEffect(Effect):

    def __init__(self, animation: Animation, render_location, section: pygame.Rect, scale=False):
        super().__init__(animation, render_location, scale)
        self.trim_rect = section

    @property
    def image(self):
        frame = super().image
        sub_frame = frame.subsurface(self.trim_rect)
        final_frame = tools.transform.get_clear_surface(frame.get_size())
        final_frame.blit(sub_frame, self.trim_rect.topleft)
        return final_frame
