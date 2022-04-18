import pygame

from externals.title_screen.settings.settings_item import SettingsItem
from sound import sounds
from tools.text import render_font_cool as Text


class Button(SettingsItem):
    def __init__(self, text, pos, result):
        super().__init__()
        self.unselected_surface = Text(text, zoom=2)
        self.selected_surface = Text(text, color1=(60, 60, 255), zoom=2)
        self.rect = pygame.Rect(pos[0], pos[1], self.unselected_surface.get_width(), self.unselected_surface.get_height())
        self.result = result

        class ButtonSprite(pygame.sprite.Sprite):
            def __init__(self, u_image, s_image, rect):
                super().__init__()
                self.rect = rect
                self.unselected_image = u_image
                self.selected_image = s_image
                self.selected = False

            @property
            def image(self):
                if self.selected:
                    return self.selected_image
                else:
                    return self.unselected_image

        self.sprite = ButtonSprite(self.unselected_surface, self.selected_surface, self.rect)
        self.add(self.sprite)

    def on_selected_change(self):
        self.sprite.selected = self.selected

    def on_click(self):
        sounds.play_sound("select")
        return self.result

    def on_left(self):
        return self.result

    def on_right(self):
        return self.result
