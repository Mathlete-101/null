import pygame

from externals.title_screen.settings.settings_item import SettingsItem
from misc.wrapped_sprite import WrappedSprite
from tools.text import render_font_cool as Text


class Switch(SettingsItem):
    def __init__(self, pos, text, starting_value):
        super().__init__()
        self.pos = pos
        self.text = text
        self.value = starting_value

        # background of the switch
        self.switch_box_off = pygame.Surface((100, 40))
        self.switch_box_off.fill((225, 225, 225))
        # the inside of the background (5 px from each edge)
        self.switch_box_off.fill((200, 200, 200), (5, 5, 90, 30))

        self.switch_box_on = pygame.Surface((100, 40))
        self.switch_box_on.fill((225, 225, 225))
        self.switch_box_on.fill((50, 210, 50), (5, 5, 90, 30))

        self.switch_box_rect = (self.pos[0], self.pos[1], 100, 40)

        # the switch itself
        self.unselected_switch = pygame.Surface((30, 30))
        self.unselected_switch.fill((255, 255, 255))
        self.selected_switch = pygame.Surface((30, 30))
        self.selected_switch.fill((60, 60, 255))
        self.switch_on_rect = (self.pos[0] + 100 - 5 - 30, self.pos[1] + 5, 30, 30)
        self.switch_off_rect = (self.pos[0] + 5, self.pos[1] + 5, 30, 30)

        # the text
        self.switch_text = Text(self.text, zoom=2)
        self.switch_text_rect = (self.pos[0], self.pos[1] - 60, self.switch_text.get_width(), self.switch_text.get_height())

        # sprites for all the above
        self.switch_box_sprite = WrappedSprite(self.switch_box, self.switch_box_rect)
        self.add(self.switch_box_sprite)
        self.switch_sprite = WrappedSprite(self.unselected_switch, self.switch_rect)
        self.add(self.switch_sprite)
        self.switch_text_sprite = WrappedSprite(self.switch_text, self.switch_text_rect)
        self.add(self.switch_text_sprite)


    def on_selected_change(self):
        super().on_selected_change()
        if self.selected:
            self.switch_sprite.image = self.selected_switch
        else:
            self.switch_sprite.image = self.unselected_switch

    @property
    def switch_rect(self):
        if self.value:
            return self.switch_on_rect
        else:
            return self.switch_off_rect

    @property
    def switch_box(self):
        if self.value:
            return self.switch_box_on
        else:
            return self.switch_box_off

    @property
    def val(self):
        return self.value

    def on_click(self):
        self.value = not self.value
        self.update_switch_position()

    def update_switch_position(self):
        self.switch_sprite.rect = self.switch_rect
        self.switch_box_sprite.image = self.switch_box

