import pygame

from controller.controller import Controller
from externals.title_screen.selector_item import SelectorItem
from tools import duple
from sound import sounds


class Selector(pygame.sprite.Group):
    """A class that generates a list of options that the use can select from. Is a pygame sprite group"""
    def __init__(self, options, location, controller: Controller, alignment="center", spacing=50, start_selected=0):
        super().__init__()
        self.options = []
        for i in range(len(options)):
            sprite = SelectorItem(options[i], duple.add(location, (0, i * spacing)), i, alignment=alignment)
            self.add(sprite)
            self.options.append(sprite)
        self.length = len(options)
        self.currently_selected_number = start_selected
        self.selected_item.selected = True
        self.controller = controller
        self._active = True

    def get_item(self, number):
        for option in self.options:
            if option.number == number:
                return option
        return None

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        self._active = value
        if value:
            self.selected_item.selected = True
        else:
            self.selected_item.selected = False

    @property
    def selected_item(self):
        return self.get_item(self.currently_selected_number)

    def update(self):
        """
        Updates the selector.
        :return: 0 if no change, 1 if down, 2 if up, and 3 if enter
        """
        super().update()
        if self.controller.start_down:
            self.selected_item.selected = False
            self.currently_selected_number = (self.currently_selected_number + 1) % len(self.options)
            self.selected_item.selected = True
            sounds.play_sound("updown")
            return 1
        elif self.controller.start_up:
            self.selected_item.selected = False
            self.currently_selected_number = (self.currently_selected_number - 1) % len(self.options)
            self.selected_item.selected = True
            sounds.play_sound("updown")
            return 2
        elif self.controller.start_enter:
            sounds.play_sound("select")
            return 3
        return 0
