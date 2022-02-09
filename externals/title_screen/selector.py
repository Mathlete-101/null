import pygame

from engine import keys
from externals.title_screen.selector_item import SelectorItem
from tools import duple


class Selector(pygame.sprite.Group):
    def __init__(self, options, location):
        super().__init__()
        self.options = []
        for i in range(len(options)):
            sprite = SelectorItem(options[i], duple.add(location, (0, i * 50)), i)
            self.add(sprite)
            self.options.append(sprite)
        self.length = len(options)
        self.currently_selected_number = 0
        self.selected_item.selected = True

    def get_item(self, number):
        for option in self.options:
            if option.number == number:
                return option
        return None

    @property
    def selected_item(self):
        return self.get_item(self.currently_selected_number)

    def update(self):
        super().update()
        if keys.down_down:
            self.selected_item.selected = False
            self.currently_selected_number = min(self.currently_selected_number + 1, self.length - 1)
            self.selected_item.selected = True
        elif keys.up_down:
            self.selected_item.selected = False
            self.currently_selected_number = max(self.currently_selected_number - 1, 0)
            self.selected_item.selected = True
