import pygame

from controller.keyboard_controller import KeyboardController
import controller.keyboard_controller as keyboard_controller
from controller.nes_controller import NESController
from engine.settings import settings
from externals.title_screen.settings.button import Button
from externals.title_screen.settings.settings_panel import SettingsPanel
from graphics import graphics
from misc.wrapped_sprite import WrappedSprite
from tools.text import render_font_cool as Text


controller_types = [
    {
        "display_name": "Keyboard: WASD / ~ 1",
        "generate_function": lambda: KeyboardController(keyboard_controller_layout=keyboard_controller.LEFT_SIDE_LAYOUT, controller_type="keyboard_1"),
        "icon": "wasd",
        "id": "keyboard_1"
    },
    {
        "display_name": "Keyboard: Arrow Keys / A S",
        "generate_function": lambda: KeyboardController(keyboard_controller_layout=keyboard_controller.STANDARD_LAYOUT, controller_type="keyboard_2"),
        "icon": "arrow_keys_secondary",
        "id": "keyboard_2"
    },
    {
        "display_name": "Keyboard: Arrow Keys / < >",
        "generate_function": lambda: KeyboardController(keyboard_controller_layout=keyboard_controller.RIGHT_SIDE_LAYOUT, controller_type="keyboard_3"),
        "icon": "arrow_keys_primary",
        "id": "keyboard_3"
    },
    {
        "display_name": "NES Controller 1",
        "generate_function": lambda: NESController(0, controller_type="nes_1"),
        "icon": "nes1",
        "id": "nes_1"
    },
    {
        "display_name": "NES Controller 2",
        "generate_function": lambda: NESController(1, controller_type="nes_2"),
        "icon": "nes2",
        "id": "nes_2"
    }
]


def find_controller_type_by_id(type_id):
    for controller_type in controller_types:
        if controller_type["id"] == type_id:
            return controller_type


def get_controller_type(controller):
    for controller_type in controller_types:
        if controller_type["id"] == controller.controller_type:
            return controller_type


def get_next_controller_type(controller_type):
    for i in range(len(controller_types)):
        if controller_types[i]["id"] == controller_type["id"]:
            return controller_types[(i + 1) % len(controller_types)]


def get_player_controller(player_number):
    from engine.game import engine
    return engine.game_controllers[player_number - 1]


def get_player_controller_type(player_number):
    return get_controller_type(get_player_controller(player_number))


def generate_controller_images(controller_type):
    return Text(controller_type["display_name"], zoom=1), graphics.get(controller_type["icon"])


class ControllerSettingsPanel(SettingsPanel):
    def __init__(self, dim, controller):
        super().__init__(dim, controller)

        self.player_1_button = Button("Player 1", self.sp((0.3, 0.2)), "player_1")
        self.add_settings_item(self.player_1_button)
        self.player_2_button = Button("Player 2", self.sp((0.6, 0.2)), "player_2")
        self.add_settings_item(self.player_2_button)

        self.player_1_icon = WrappedSprite(pygame.Surface((0, 0)), self.sp((0.35, 0.3)))
        self.player_1_text = WrappedSprite(pygame.Surface((0, 0)), self.sp((0.35, 0.5)))
        self.player_2_icon = WrappedSprite(pygame.Surface((0, 0)), self.sp((0.65, 0.3)))
        self.player_2_text = WrappedSprite(pygame.Surface((0, 0)), self.sp((0.65, 0.5)))
        self.add([self.player_1_icon, self.player_1_text, self.player_2_icon, self.player_2_text])

        self.instructions = WrappedSprite(Text("Press enter to change controller type", zoom=2), self.sp((0.3, 0.65)))
        self.add(self.instructions)

        self.back_button = Button("Back", self.sp((0.3, 0.8)), "back")
        self.add_settings_item(self.back_button)
        self.initialized = False

    def set_controller_icons(self):
        self.player_1_text.image, self.player_1_icon.image = generate_controller_images(get_player_controller_type(1))
        self.player_2_text.image, self.player_2_icon.image = generate_controller_images(get_player_controller_type(2))

    def on_item_click(self, result):
        if result.split("_")[0] == "player":
            player_number = int(result.split("_")[1])
            new_controller_type = get_next_controller_type(get_controller_type(get_player_controller(player_number)))
            new_controller = new_controller_type["generate_function"]()
            get_player_controller(player_number).controllers = [new_controller]
            self.set_controller_icons()
            settings.set("controllers.player_" + str(player_number), new_controller_type["id"])
        elif result == "back":
            return True
        return False

    def update(self):
        if not self.initialized:
            self.initialized = True
            self.set_controller_icons()
        return super().update()




