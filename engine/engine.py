import os.path

import pygame
from stopwatch import Stopwatch

import tools.text
from assembler.levels.levels import load_level, check_level_exists
from engine import keys
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

        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        #initialize the font
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
                self.screen.blit(self.current_level.render(),
                            (max(- len(self.current_level.main) * 42 + self.screen.get_width(), min(0, 0 - (self.current_level.player.render_location[0] - self.screen.get_width() // 2))),
                             max(- len(self.current_level.main[0]) * 42 + self.screen.get_height(), min(0, 0 - (self.current_level.player.render_location[1] - self.screen.get_height() // 2)))))

                # HUD
                text = format(self.score, "06")
                self.screen.blit(render_font_cool(text), (10, 10))

            clock.tick(fps)



            # Update the keypress variables
            keys.a_down = False
            keys.b_down = False
            keys.up_down = False
            keys.down_down = False
            keys.left_down = False
            keys.right_down = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:

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
                    elif event.key == pygame.K_RIGHT:
                        keys.right = False
                    elif event.key == pygame.K_DOWN:
                        keys.down = False
                    elif event.key == pygame.K_a:
                        keys.a = False
                    elif event.key == pygame.K_b:
                        keys.b = False
                    elif event.key == pygame.K_e:
                        fps = 30
            if self.current_level_number > 0:
                self.current_level.update()

engine = Engine()
