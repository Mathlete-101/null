import pygame

from externals.title_screen.settings.settings_item import SettingsItem
from sound import sounds
from tools.duple import ScreenPosition


class SettingsPanel(pygame.sprite.Group):
    def __init__(self, dim, controller):
        super().__init__()
        self.dim = dim
        self.sp = ScreenPosition(dim)
        self.controller = controller
        self._active = False
        self.items: list[SettingsItem] = []
        self.selected_item_number = 0
        self.item_names = []

    def on_item_click(self, result):
        """Return True to quit, false to continue"""
        if result == "back":
            return True
        return False

    def on_item_left(self, result):
        pass

    def on_item_right(self, result):
        pass

    def select_unselect(self, select, unselect):
        self.items[select].selected = True
        self.items[unselect].selected = False

    @property
    def selected_item(self):
        return self.items[self.selected_item_number]

    @property
    def selected_item_name(self):
        return self.item_names[self.selected_item_number]

    def add_settings_item(self, item, name=None):
        self.add(item)
        self.items.append(item)
        if name is not None:
            self.item_names.append(name)
        else:
            self.item_names.append(len(self.items) - 1)

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        self._active = value
        if value:
            self.selected_item_number = 0
            self.selected_item.selected = True
        else:
            self.selected_item.selected = False

    def update(self):
        if self.controller.start_down:
            last_selected = self.selected_item_number
            self.selected_item_number += 1
            self.selected_item_number %= len(self.items)
            self.select_unselect(self.selected_item_number, last_selected)
            sounds.play_sound("updown")
        elif self.controller.start_up:
            last_selected = self.selected_item_number
            self.selected_item_number -= 1
            self.selected_item_number %= len(self.items)
            self.select_unselect(self.selected_item_number, last_selected)
            sounds.play_sound("updown")
        elif self.controller.start_enter:
            return self.on_item_click(self.selected_item.on_click())
        elif self.controller.start_left:
            self.on_item_left(self.selected_item.on_left())
        elif self.controller.start_right:
            self.on_item_right(self.selected_item.on_right())
        return False

    @property
    def exit(self):
        return True

    @property
    def exit(self):
        return False