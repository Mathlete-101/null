import time

import pygame
from engine.game import engine

if not pygame.font:
    print('Warning: fonts disabled')
if not pygame.mixer:
    print('Warning: sounds disabled')


def main():
    engine.start()

    # let sounds finish playing
    time.sleep(0.05)


if __name__ == '__main__':
    main()
