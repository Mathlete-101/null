import pygame.sprite

import tools


class SelectorItem(pygame.sprite.Sprite):
    def __init__(self, text, location, number):
        super().__init__()
        self.off_image = tools.transform.scale_factor(tools.text.render_font_cool(text), 2)
        self.on_image = tools.transform.scale_factor(tools.text.render_font_cool(text, color1=(60, 60, 255)), 2)
        self.rect = pygame.Rect(location[0] - self.on_image.get_size()[0] / 2, location[1], self.off_image.get_size()[0], self.off_image.get_size()[1])
        self.selected = False
        self.number = number

    @property
    def image(self):
        if self.selected:
            return self.on_image
        else:
            return self.off_image

    def update(self):
        pass