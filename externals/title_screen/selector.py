import pygame

from controller.controller import Controller
from engine import keys
from externals.title_screen.selector_item import SelectorItem
from tools import duple
from sound import sounds


class Selector(pygame.sprite.Group):
    def __init__(self, options, location, controller: Controller):
        super().__init__()
        self.options = []
        for i in range(len(options)):
            sprite = SelectorItem(options[i], duple.add(location, (0, i * 50)), i)
            self.add(sprite)
            self.options.append(sprite)
        self.length = len(options)
        self.currently_selected_number = 0
        self.selected_item.selected = True
        self.controller = controller

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
        if self.controller.start_down:
            self.selected_item.selected = False
            self.currently_selected_number = (self.currently_selected_number + 1) % len(self.options)
            self.selected_item.selected = True
            sounds.play_sound("updown")
        elif self.controller.start_up:
            self.selected_item.selected = False
            self.currently_selected_number = (self.currently_selected_number - 1) % len(self.options)
            self.selected_item.selected = True
            sounds.play_sound("updown")
        elif self.controller.start_enter:
            sounds.play_sound("select")
