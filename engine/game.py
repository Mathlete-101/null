import os.path

import pygame

from assembler import assembler
import tools.text
from assembler.levels.levels import load_level, check_level_exists, get_level_dir, get_controller_save_path
from controller.full_keyboard_controller import FullKeyboardController
from controller.keyboard_controller import KeyboardController
from controller.merged_controller import MergedController
from controller.nes_controller import NESController
from engine import settings
from engine.controller_override import ControllerOverride
from engine.settings import settings
from externals.game_over.game_over import GameOver
from externals.leaderboard.leaderboard import Leaderboard
from externals.recording_complete.recording_complete import RecordingComplete
from externals.title_screen.title_screen import TitleScreen
from sound import sounds
from tools.text import render_font_cool
import externals.title_screen.settings.controller_settings_panel as csp


class Engine:
    def __init__(self):
        self.current_level_number = 0
        self.current_level = None
        self.level_builder_player_location = None
        self.score = 0
        self.difficulty = 1
        self.assistive_signs = True
        self.controller_override: ControllerOverride or None = None
        self.bar_length = 120
        self.primary_controller = MergedController([KeyboardController(), NESController(0), NESController(1)])
        self.controller_block_time = 0
        self.game_controllers = {
            0: MergedController([csp.find_controller_type_by_id(settings.get("controllers.player_1"))["generate_function"]()]),
            1: MergedController([csp.find_controller_type_by_id(settings.get("controllers.player_2"))["generate_function"]()])
        }
        self.full_keyboard_controller = FullKeyboardController()

        # Start pygame
        pygame.init()
        pygame.mixer.init()



        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        # Load all the assets
        assembler.assemble()

        # initialize joysticks
        pygame.joystick.init()
        self.pygame_joystick_objects = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        self.main_nes_controller = None

        # initialize the font
        # this has to be here because pygame.init() is called above
        tools.text.minecraft_font = pygame.font.Font(os.path.join("resources", "misc", "minecraft_font.ttf"), 16)

        # make sure the volumes are set correctly
        sounds.update_volume()

        # Make the loading screen
        self.loading_screen = pygame.Surface(self.screen.get_size())
        self.initialize_loading_surface()
        self.display_loading()

        # Make the title screen
        self.title_screen = TitleScreen(self.screen.get_size(), self.alpha_controller)

        # Placeholder for leaderboard, etc
        self.leaderboard = None
        self.recording_complete = None

        # Game type
        # Either "single_player" or "two_player" or "level_builder" or "demo/record" or "demo/replay"
        self.game_type = "single_player"

        # Bypass startup screens to get where I want to be
        # For debugging
        # Set this to the number of the level minus 1
        # self.current_level_number = 10
        # self.difficulty = 4
        # self.next_level()

    def initialize_loading_surface(self):
        self.loading_screen.fill((60, 60, 80))
        self.loading_screen.blit(render_font_cool("Loading..."), (10, self.screen.get_size()[1] - 30))

    @property
    def current_players(self):
        return self.current_level.players

    @property
    def joysticks(self):
        return [self.primary_controller, self.game_controllers[0], self.game_controllers[1], self.full_keyboard_controller]

    def display_loading(self):
        self.screen.blit(self.loading_screen, (0, 0))

    def display_player_bars(self, player, x, laser_color):

        # The part of the hud with the laser bar
        self.screen.fill((255, 255, 255), pygame.rect.Rect(x - 2, self.screen.get_height() - 22, self.bar_length + 4, 14))
        self.screen.fill(laser_color, pygame.rect.Rect(x, self.screen.get_height() - 20, self.bar_length - (
                self.bar_length / player.laser_recharge_time) * player.laser_cooldown, 10))

        # The part of the hud with the movement bar
        if player.movement_belt:
            self.screen.fill((255, 255, 255), pygame.rect.Rect(x - 2, self.screen.get_height() - 42, self.bar_length + 4, 14))
            self.screen.fill((142, 6, 6), pygame.rect.Rect(x, self.screen.get_height() - 40, (
                    self.bar_length / player.max_movement_belt_charges) * player.movement_belt_charges, 10))
            for i in range(player.max_movement_belt_charges - 1):
                self.screen.fill((255, 255, 255),
                                 pygame.rect.Rect(x - 2 + self.bar_length / player.max_movement_belt_charges * (i + 1),
                                                  self.screen.get_height() - 40, 4, 2))
                self.screen.fill((255, 255, 255),
                                 pygame.rect.Rect(x - 2 + self.bar_length / player.max_movement_belt_charges * (i + 1),
                                                  self.screen.get_height() - 32, 4, 2))

    def next_level(self):
        def check_save_controls():
            # Save the player controller recordings if nessecary
            if self.game_type == "demo/record" and self.current_level_number > 1:
                for i in range(len(self.current_level.players)):
                    self.game_controllers[i].save(
                        get_controller_save_path(self.game_type, str(self.current_level_number - 1), i))
        self.display_loading()
        pygame.display.flip()
        self.current_level_number += 1
        if check_level_exists(self.game_type, str(self.current_level_number)):
            sounds.stop_music()
            if self.current_level:
                self.current_level.prepare_for_destruction()
            check_save_controls()
            # Generate and prepare the level
            self.current_level = load_level(self.game_type, str(self.current_level_number))
            if self.game_type != "level_builder":
                self.current_level.null_speed = 30 - (5 * self.difficulty)
                for i in range(len(self.current_level.players)):
                    self.game_controllers[i].clear_movement_belt()
                    self.current_level.players[i].controller = self.game_controllers[i]
                    if self.game_type == "demo/record":
                        self.game_controllers[i].reset_recording()
                    if self.game_type == "demo/replay":
                        self.game_controllers[i].load(get_controller_save_path(self.game_type, str(self.current_level_number), i))

                if self.current_level.null_speed <= 30:
                    sounds.play_music("dont_fall_behind_" + str(self.current_level.null_speed))
            else:
                self.current_level.players[0].controller = self.full_keyboard_controller

        else:
            check_save_controls()
            if self.game_type.split("/")[0] == "demo":
                self.go_to_recording_complete()
            else:
                game_over = GameOver(self.screen.get_size(), "Game Complete")
                game_over.play_animation(self.screen)
                self.go_to_leaderboard()

    def block_controllers(self, time):
        self.controller_block_time = time

    def end_game(self):
        game_over = GameOver(self.screen.get_size(), "Game Over")
        game_over.play_animation(self.screen)
        self.go_to_leaderboard()

    def go_to_leaderboard(self):
        self.leaderboard = Leaderboard(self.screen.get_size())
        self.current_level_number = -1

    def go_to_recording_complete(self):
        self.recording_complete = RecordingComplete(self.screen.get_size(), self.primary_controller)
        self.current_level_number = -2

    def restart(self):
        self.current_level_number = 0
        self.title_screen.reset()
        self.score = 0
        self.primary_controller.clear()

    @property
    def alpha_controller(self):
        if len(self.joysticks) > 0:
            return MergedController([self.joysticks[0], self.primary_controller])
        else:
            return self.primary_controller

    def get_controller(self, number):
        return self.game_controllers[number]

    def start(self):
        # Initialize joysticks

        clock = pygame.time.Clock()

        fps = 30
        while True:
            pygame.display.flip()
            if self.current_level_number == 0:
                self.title_screen.update()
                self.screen.blit(self.title_screen.render(), (0, 0))
            elif self.current_level_number == -1:
                self.leaderboard.update()
                self.screen.blit(self.leaderboard.render(), (0, 0))
            elif self.current_level_number == -2:
                self.recording_complete.update()
                self.screen.blit(self.recording_complete.render(), (0, 0))
            else:
                # self.screen.blit(self.current_level.get_parallax_subsurface(), )
                coords = (
                    max(- len(self.current_level.main) * 42 + self.screen.get_width(),
                        min(0, 0 - (self.current_level.players[0].render_location[0] - self.screen.get_width() // 2))),
                    max(- len(self.current_level.main[0]) * 42 + self.screen.get_height(),
                        min(0, 0 - (self.current_level.players[0].render_location[1] - self.screen.get_height() // 2))))
                self.screen.blit(self.current_level.render(), coords)

                # HUD
                text = format(self.score, "06")
                self.screen.blit(render_font_cool(text), (10, 10))

                if self.game_type != "level_builder":
                    self.display_player_bars(self.current_players[0], 10, (0, 162, 232))
                    if len(self.current_level.players) == 2:
                        self.display_player_bars(self.current_players[1], self.screen.get_width() - 10 - self.bar_length, (232, 162, 0))
                    elif self.game_type == "two_player":
                        raise Exception("you oaf. You forgot to set player_count = 2 in meta.json for level", self.current_level.level_name)

            clock.tick(fps)

            # Update Controllers
            if self.controller_block_time == 0:
                for event in pygame.event.get():
                    if event.type == pygame.JOYDEVICEADDED or pygame.JOYDEVICEREMOVED:
                        pass

                    if event.type == pygame.QUIT:
                        return
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        return
                    else:
                        for controller in self.joysticks:
                            if controller.uses_event(event):
                                controller.add_event(event)

                for controller in self.joysticks:
                    controller.update()
            else:
                self.controller_block_time -= 1
                pygame.event.get()

            if self.current_level_number > 0:
                self.current_level.update()

    def override_controller(self, controller_override):
        self.controller_override = controller_override


engine = Engine()
