import pygame


class SettingsItem(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self._selected = False

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        if value != self._selected:
            self._selected = value
            self.on_selected_change()

    def on_selected_change(self):
        pass

    def on_click(self):
        pass
