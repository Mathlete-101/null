import pygame

import tools.text
from tools import duple


class GameOver(pygame.sprite.Group):
    def __init__(self, dim, text):
        super().__init__()
        self.frame = pygame.Surface(dim)
        self.frame.fill((60, 60, 80))
        self.sprite_storage = tools.text.get_spaced_sprites(text, duple.scale(duple.subtract(dim, tools.text.get_spaced_sprites_size(text, 0)), 1/2), 0).sprites()

    def play_animation(self, screen):
        clock = pygame.time.Clock()
        for sprite in self.sprite_storage:
            clock.tick(4)
            self.add(sprite)
            self.draw(self.frame)
            screen.blit(self.frame, (0, 0))
            pygame.display.flip()
        clock.tick(1)
        clock.tick(1)
        clock.tick(1)
        clock.tick(1)
        clock.tick(1)
        clock.tick(1)

        # Reset the events so that keypresses don't work
        pygame.event.clear(pygame.KEYDOWN)


