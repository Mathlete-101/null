import pygame

import tools.text
from tools import duple


class GameOver(pygame.sprite.Group):
    def __init__(self, size, text):
        super().__init__()
        self.frame = pygame.Surface(size)
        self.frame.fill((60, 60, 80))
        self.sprite_storage = tools.text.get_monospaced_sprites(text, duple.scale(duple.subtract(size, tools.text.get_monospaced_sprites_size(text, 40)), 1/2), 40).sprites()

    def play_animation(self, screen):
        clock = pygame.time.Clock()
        for sprite in self.sprite_storage:
            clock.tick(2)
            self.add(sprite)
            self.draw(self.frame)
            screen.blit(self.frame, (0, 0))
            pygame.display.flip()
        clock.tick(1)
        clock.tick(1)
        clock.tick(1)

        # Reset the events so that keypresses don't work
        pygame.event.clear(pygame.KEYDOWN)


