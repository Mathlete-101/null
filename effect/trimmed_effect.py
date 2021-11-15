import pygame
import tools

from animation.animation import Animation
from effect.effect import Effect


class TrimmedEffect(Effect):

    def __init__(self, animation: Animation, render_location, section: pygame.Rect, scale=False):
        super().__init__(animation, render_location, scale)
        self.rect = section

    def get_frame(self):
        frame = super().get_frame()
        print(frame.get_size())
        sub_frame = frame.subsurface(self.rect)
        final_frame = tools.transform.get_clear_surface(frame.get_size())
        final_frame.blit(sub_frame, self.rect.topleft)
        return final_frame
