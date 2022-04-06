import os.path

import pygame
from stopwatch import Stopwatch

from assembler import assembler
import tools.text
from assembler.levels.levels import load_level, check_level_exists
from engine import keys
from engine.controller_override import ControllerOverride
from externals.game_over.game_over import GameOver
from externals.leaderboard.leaderboard import Leaderboard
from externals.title_screen.title_screen import TitleScreen
from tools.text import render_font_cool


class Engine:
    def __init__(self):
        self.current_level_number = 0
        self.current_level = None
        self.score = 0
        self.difficulty = 1
        self.controller_override: ControllerOverride or None = None

        pygame.init()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        assembler.assemble()

        # initialize the font
        tools.text.minecraft_font = pygame.font.Font(os.path.join("resources", "misc", "minecraft_font.ttf"), 16)

        # Make the loading screen
        self.loading_screen = pygame.Surface(self.screen.get_size())
        self.loading_screen.fill((60, 60, 80))
        self.loading_screen.blit(render_font_cool("Loading..."), (10, self.screen.get_size()[1] - 30))
        self.display_loading()

        # Make the title screen
        self.title_screen = TitleScreen(self.screen.get_size())

        # Placeholder for leaderboard
        self.leaderboard = None

        # Bypass startup screens to get where I want to be
        # For debugging
        # Set this to the number of the level minus 1
        self.current_level_number = 8
        self.difficulty = -1
        self.next_level()

    @property
    def current_player(self):
        return self.current_level.player

    def display_loading(self):
        self.screen.blit(self.loading_screen, (0, 0))

    def next_level(self):
        self.display_loading()
        pygame.display.flip()
        self.current_level_number += 1
        if check_level_exists(str(self.current_level_number)):
            if self.current_level:
                self.current_level.prepare_for_destruction()
            self.current_level = load_level(str(self.current_level_number))
            self.current_level.null_speed = 30 - (5 * self.difficulty)
        else:
            game_over = GameOver(self.screen.get_size(), "Game Complete")
            game_over.play_animation(self.screen)
            self.go_to_leaderboard()

    def end_game(self):
        game_over = GameOver(self.screen.get_size(), "Game Over")
        game_over.play_animation(self.screen)
        self.go_to_leaderboard()

    def go_to_leaderboard(self):
        self.leaderboard = Leaderboard(self.screen.get_size())
        self.current_level_number = -1

    def start(self):
        # Initialize joysticks
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

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
            else:
                # self.screen.blit(self.current_level.get_parallax_subsurface(), )
                coords = (
                    max(- len(self.current_level.main) * 42 + self.screen.get_width(),
                        min(0, 0 - (self.current_level.player.render_location[0] - self.screen.get_width() // 2))),
                    max(- len(self.current_level.main[0]) * 42 + self.screen.get_height(),
                        min(0, 0 - (self.current_level.player.render_location[1] - self.screen.get_height() // 2))))
                self.screen.blit(self.current_level.render(), coords)

                # HUD
                text = format(self.score, "06")
                self.screen.blit(render_font_cool(text), (10, 10))
                bar_length = 120

                # The part of the hud with the laser bar
                self.screen.fill((255, 255, 255), pygame.rect.Rect(8, self.screen.get_height() - 22, bar_length + 4, 14))
                self.screen.fill((0, 162, 232), pygame.rect.Rect(10, self.screen.get_height() - 20, bar_length - (bar_length / self.current_player.laser_recharge_time) * self.current_player.laser_cooldown, 10))

                # The part of the hud with the movement bar
                if self.current_player.movement_belt:
                    self.screen.fill((255, 255, 255), pygame.rect.Rect(8, self.screen.get_height() - 42, bar_length + 4, 14))
                    self.screen.fill((142, 6, 6), pygame.rect.Rect(10, self.screen.get_height() - 40, (bar_length / self.current_player.max_movement_belt_charges) * self.current_player.movement_belt_charges, 10))
                    for i in range(self.current_player.max_movement_belt_charges - 1):
                        self.screen.fill((255, 255, 255), pygame.rect.Rect(8 + bar_length / self.current_player.max_movement_belt_charges * (i + 1), self.screen.get_height() - 40, 4, 2))
                        self.screen.fill((255, 255, 255), pygame.rect.Rect(8 + bar_length / self.current_player.max_movement_belt_charges * (i + 1), self.screen.get_height() - 32, 4, 2))

            clock.tick(fps)

            # Update the keypress variables
            keys.a_down = False
            keys.b_down = False
            keys.up_down = False
            keys.down_down = False
            keys.left_down = False
            keys.right_down = False
            keys.left_up = False
            keys.right_up = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_UP:
                        keys.up = True
                        keys.down = False
                        keys.up_down = True
                    elif event.key == pygame.K_LEFT:
                        keys.left = True
                        keys.right = False
                        keys.left_down = True
                    elif event.key == pygame.K_RIGHT:
                        keys.right = True
                        keys.left = False
                        keys.right_down = True
                    elif event.key == pygame.K_DOWN:
                        keys.down = True
                        keys.up = False
                        keys.down_down = True
                    elif event.key == pygame.K_a:
                        keys.a = True
                        keys.a_down = True
                    elif event.key == pygame.K_b:
                        keys.b = True
                        keys.b_down = True
                    elif event.key == pygame.K_e:
                        fps = 3
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        keys.up = False
                    elif event.key == pygame.K_LEFT:
                        keys.left = False
                        keys.left_up = True
                    elif event.key == pygame.K_RIGHT:
                        keys.right = False
                        keys.right_up = True
                    elif event.key == pygame.K_DOWN:
                        keys.down = False
                    elif event.key == pygame.K_a:
                        keys.a = False
                    elif event.key == pygame.K_b:
                        keys.b = False
                    elif event.key == pygame.K_e:
                        fps = 30
                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 1:
                        keys.a = True
                        keys.a_down = True
                    elif event.button == 2:
                        keys.b = True
                        keys.b_down = True
                elif event.type == pygame.JOYBUTTONUP:
                    if event.button == 1:
                        keys.a = False
                    elif event.button == 2:
                        keys.b = False
                elif event.type == pygame.JOYAXISMOTION:
                    if event.axis == 4:
                        if abs(event.value) > 0.1:
                            if event.value > 0:
                                keys.down = True
                                keys.up = False
                                keys.down_down = True
                            else:
                                keys.up = True
                                keys.down = False
                                keys.up_down = True
                        else:
                            keys.up = False
                            keys.down = False
                    elif event.axis == 0:
                        if abs(event.value) > 0.1:
                            change_value = event.value * keys.last_x_axis
                            if event.value < 0:
                                keys.left = True
                                keys.right = False
                                keys.left_down = True
                                if change_value < -0.01:
                                    keys.right_up = True
                            else:
                                keys.right = True
                                keys.left = False
                                keys.right_down = True
                                if change_value < -0.01:
                                    keys.left_up = True
                        else:
                            keys.right = False
                            keys.left = False
                            keys.right_up = True
                            keys.left_up = True
                        keys.last_x_axis = event.value

            # Check for double clicks
            keys.last_left_down += 1
            keys.last_right_down += 1
            keys.last_left_up += 1
            keys.last_right_up += 1

            if keys.left_down:
                keys.last_left_down = 0
            if keys.right_down:
                keys.last_right_down = 0
            if keys.left_up:
                keys.last_left_up = 0
            if keys.right_up:
                keys.last_right_up = 0

            if keys.left_down and keys.last_left_down < keys.double_click_time and keys.last_left_up < keys.double_click_time:
                keys.left_double_click = True
            else:
                keys.left_double_click = False

            if keys.right_down and keys.last_right_down < keys.double_click_time and keys.last_right_up < keys.double_click_time:
                keys.right_double_click = True
            else:
                keys.right_double_click = False




            if self.current_level_number > 0:
                self.current_level.update()

    def override_controller(self, controller_override):
        self.controller_override = controller_override


engine = Engine()
