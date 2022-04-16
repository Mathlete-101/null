import os.path

import pygame

import tools.transform
from controller.controller import Controller
from externals.title_screen.selector import Selector
from externals.title_screen.settings.settings import Settings
from misc.wrapped_sprite import WrappedSprite
from graphics import graphics
from tools.text import render_font_cool as Text
import tools.duple


def zoom_in(image):
    return tools.transform.scale_factor(image, 3)


class TitleScreen:
    def __init__(self, size, controller):
        self.background_surface = pygame.Surface(size)
        self.background_surface.fill((60, 60, 80))
        self.render_surface = pygame.Surface(size)
        self.render_surface.blit(self.background_surface, (0, 0))
        self.first_options = Selector(["1 Player", "2 Player", "Instructions", "Settings", "Quit"], (size[0] / 2, size[1] * 2 / 3), controller)
        self.second_options = Selector(["Easy", "Medium", "Hard", "Really Hard", "Impossible"], (size[0] / 2, size[1] * 2 / 3), controller)
        logo = tools.transform.scale_factor(pygame.image.load(os.path.join("resources", "images", "misc", "logo.png")), 12)
        self.logo = pygame.sprite.Group(WrappedSprite(logo, ((size[0] - logo.get_size()[0]) / 2, (size[1] - logo.get_size()[1]) / 4)))
        self.logo.draw(self.render_surface)
        self.settings = Settings(size, controller)
        self.state = 0
        self.controller: Controller = controller

        # Generates a helpful 3x3 array for all True
        full_surroundings = [[True for x in range(3)] for x in range(3)]

        def fix_units(a, b):
            return a * size[0]/1366, b * size[1]/768

        # The instruction sheet
        self.instructions = pygame.sprite.Group()
        self.instructions.add(WrappedSprite(Text("1. Get here"), fix_units(50, 100)))
        door_graphic = tools.transform.get_clear_surface((42, 84))
        door_graphic.blit(graphics.get("door_exit").get(), (0, 0))
        door_graphic.blit(graphics.get("platform_cross").get_with_edge(full_surroundings), (0, 42))
        door_graphic = zoom_in(door_graphic)
        self.instructions.add(WrappedSprite(door_graphic, fix_units(100, 175)))
        self.instructions.add(WrappedSprite(Text("and press B to go to the next level."), fix_units(50, 450)))

        self.instructions.add(WrappedSprite(Text("2. If your way is blocked by these"), fix_units(450, 100)))
        self.instructions.add(WrappedSprite(zoom_in(graphics.get("force_field").get()), fix_units(500, 150)))
        self.instructions.add(WrappedSprite(Text("press B to shoot these"), fix_units(450, 300)))
        self.instructions.add(WrappedSprite(zoom_in(graphics.get("energy_receiver_time").get()), fix_units(500, 350)))
        self.instructions.add(WrappedSprite(zoom_in(graphics.get("energy_receiver_toggle").get()), fix_units(646, 350)))
        self.instructions.add(WrappedSprite(Text("until it's not anymore."), fix_units(450, 500)))

        self.instructions.add(WrappedSprite(Text("3. Get these for extra points."), fix_units(850, 100)))
        self.instructions.add(WrappedSprite(zoom_in(graphics.get("data_stick_1").get()), fix_units(900, 150)))
        self.instructions.add(WrappedSprite(zoom_in(graphics.get("data_stick_2").get()), fix_units(900, 250)))
        self.instructions.add(WrappedSprite(zoom_in(graphics.get("data_stick_3").get()), fix_units(900, 350)))

        self.instructions.add(WrappedSprite(Text("and above all"), fix_units(200, 600)))
        self.instructions.add(WrappedSprite(zoom_in(Text("DON'T FALL BEHIND")), fix_units(150, 650)))
        self.instructions.add(WrappedSprite(Text("press A to return"), fix_units(900, 675)))

    def render(self):
        if self.state == 0:
            self.first_options.clear(self.render_surface, self.background_surface)
            self.first_options.draw(self.render_surface)
        elif self.state == 1:
            self.second_options.clear(self.render_surface, self.background_surface)
            self.second_options.draw(self.render_surface)
            # self.logo.draw(self.render_surface)
        elif self.state == 2:
            self.instructions.clear(self.render_surface, self.background_surface)
            self.instructions.draw(self.render_surface)
        elif self.state == 3:
            self.settings.clear(self.render_surface, self.background_surface)
            self.settings.draw(self.render_surface)
        return self.render_surface

    def update(self):

        # It's Turing Time
        # Basically just a bunch of menu logic
        # TODO: add more menu logic
        if self.state == 0:
            self.first_options.update()
            if self.controller.start_enter:
                if self.first_options.currently_selected_number == 0:
                    self.state = 1
                    self.first_options.clear(self.render_surface, self.background_surface)
                    from engine.game import engine
                    engine.game_type = "single_player"
                elif self.first_options.currently_selected_number == 1:
                    self.state = 1
                    self.first_options.clear(self.render_surface, self.background_surface)
                    from engine.game import engine
                    engine.game_type = "two_player"
                elif self.first_options.currently_selected_number == 2:
                    self.state = 2
                    self.first_options.clear(self.render_surface, self.background_surface)
                    self.logo.clear(self.render_surface, self.background_surface)
                elif self.first_options.currently_selected_number == 3:
                    self.state = 3
                    self.first_options.clear(self.render_surface, self.background_surface)
                    self.logo.clear(self.render_surface, self.background_surface)
                else:
                    # quit the game, if it isn't clear
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        elif self.state == 1:
            self.second_options.update()
            if self.controller.start_enter:
                from engine.game import engine
                engine.difficulty = self.second_options.currently_selected_number
                engine.next_level()
        elif self.state == 2:
            if self.controller.start_enter:
                self.state = 0
                self.instructions.clear(self.render_surface, self.background_surface)
                self.logo.draw(self.render_surface)
        elif self.state == 3:
            if self.settings.update():
                self.state = 0
                self.settings.clear(self.render_surface, self.background_surface)
                self.logo.draw(self.render_surface)

