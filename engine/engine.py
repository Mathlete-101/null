import pygame

from assembler.levels.levels import levels
from engine import keys
from level.level import Level


def start():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    clock = pygame.time.Clock()

    current_level: Level = levels["1"]

    fps = 30
    while True:
        pygame.display.flip()
        screen.blit(current_level.render(), (min(0, 0 - (current_level.player.render_location[0] - screen.get_width()//2)), 0))
        clock.tick(fps)
        font = pygame.font.SysFont('Courier New', 12, True)
        screen.blit(font.render(str(round(clock.get_fps(), 2)), False, (255, 255, 0)), (10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_UP:
                    keys.up = True
                    keys.down = False
                elif event.key == pygame.K_LEFT:
                    keys.left = True
                    keys.right = False
                elif event.key == pygame.K_RIGHT:
                    keys.right = True
                    keys.left = False
                elif event.key == pygame.K_DOWN:
                    keys.down = True
                    keys.up = False
                elif event.key == pygame.K_a:
                    keys.a = True
                elif event.key == pygame.K_b:
                    keys.b = True
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

        current_level.update()
