import pygame

from externals.title_screen.settings.settings_item import SettingsItem
from misc.wrapped_sprite import WrappedSprite
from sound import sounds
from tools.text import render_font_cool as Text


class Slider(SettingsItem):
    def __init__(self, length, units, pos, val, max_disp, min_disp):
        super().__init__()
        self.length = length
        self.units = units
        self.pos = pos
        self.val = val
        self.max_disp = max_disp
        self.min_disp = min_disp

        # Create the slider bar
        self.slider_bar = pygame.Surface((self.length, 10))
        self.slider_bar.fill((200, 200, 200))
        self.slider_bar_rect = (self.pos[0], self.pos[1] - 5, self.length, 10)
        self.add(WrappedSprite(self.slider_bar, self.slider_bar_rect))

        # Create little vertical lines at the ends of the slider bar
        self.slider_bar_end_lines = pygame.Surface((5, 20))
        self.slider_bar_end_lines.fill((200, 200, 200))
        self.slider_bar_end_lines_rect = (self.pos[0] - 5, self.pos[1] - 10, 5, 20)
        self.slider_bar_end_lines_rect_2 = (self.pos[0] + self.length, self.pos[1] - 10, 5, 20)
        self.add(WrappedSprite(self.slider_bar_end_lines, self.slider_bar_end_lines_rect))
        self.add(WrappedSprite(self.slider_bar_end_lines, self.slider_bar_end_lines_rect_2))

        self.unselected_handle_surface = pygame.Surface((20, 30))
        self.unselected_handle_surface.fill((255, 255, 255))
        self.selected_handle_surface = pygame.Surface((20, 30))
        self.selected_handle_surface.fill((60, 60, 255))
        self.handle_rect = (pos[0] - 5, pos[1] - 15, 10, 10)
        self.handle_sprite = WrappedSprite(self.unselected_handle_surface, self.handle_rect)
        self.add(self.handle_sprite)


        # Create the text
        min_text_surface = Text(self.min_disp)
        min_text_rect = (self.pos[0] - min_text_surface.get_width() / 2, self.pos[1] + 30, min_text_surface.get_width(), min_text_surface.get_height())
        self.add(WrappedSprite(min_text_surface, min_text_rect))
        max_text_surface = Text(self.max_disp)
        max_text_rect = (self.pos[0] + self.length - max_text_surface.get_width() / 2, self.pos[1] + 30, max_text_surface.get_width(), max_text_surface.get_height())
        self.add(WrappedSprite(max_text_surface, max_text_rect))

        # Set the slider positions properly
        self.set_slider_positions()

    def set_slider_positions(self):
        self.handle_sprite.rect.x = self.pos[0] + self.val * (self.length / self.units) - 5

    def on_click(self):
        self.slider_up()

    def slider_up(self):
        sounds.play_sound("test_tone")
        if self.val < self.units:
            self.val += 1
        else:
            self.val = 0
        self.set_slider_positions()

    def slider_down(self):
        sounds.play_sound("test_tone")
        if self.val > 0:
            self.val -= 1
        else:
            self.val = self.units
        self.set_slider_positions()

    def on_selected_change(self):
        if self.selected:
            self.handle_sprite.image = self.selected_handle_surface
        else:
            self.handle_sprite.image = self.unselected_handle_surface




