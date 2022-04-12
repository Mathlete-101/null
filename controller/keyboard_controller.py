import pygame

from controller.controller import Controller


class KeyboardController(Controller):

    def __init__(self):
        super().__init__()
        self.a = False
        self.a_down = False
        self.s = False
        self.s_down = False
        self.up_arrow = False
        self.up_arrow_down = False
        self.down_arrow = False
        self.down_arrow_down = False
        self.left_arrow = False
        self.left_arrow_down = False
        self.right_arrow = False
        self.right_arrow_down = False
        self.double_tap_counter = 0
        self.last_arrow_left_or_right = ''

    def update(self):
        if self.double_tap_counter > 0:
            self.double_tap_counter -= 1

        # Reset variables ending in _down to false
        self.a_down = False
        self.s_down = False
        self.up_arrow_down = False
        self.down_arrow_down = False
        self.left_arrow_down = False
        self.right_arrow_down = False

        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.a = True
                    self.a_down = True
                elif event.key == pygame.K_s:
                    self.s = True
                    self.s_down = True
                elif event.key == pygame.K_UP:
                    self.up_arrow = True
                    self.up_arrow_down = True
                elif event.key == pygame.K_DOWN:
                    self.down_arrow = True
                    self.down_arrow_down = True
                elif event.key == pygame.K_LEFT:
                    self.left_arrow = True
                    self.left_arrow_down = True
                    self.last_arrow_left_or_right = 'left'
                elif event.key == pygame.K_RIGHT:
                    self.right_arrow = True
                    self.right_arrow_down = True
                    self.last_arrow_left_or_right = 'right'
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.a = False
                elif event.key == pygame.K_s:
                    self.s = False
                elif event.key == pygame.K_UP:
                    self.up_arrow = False
                elif event.key == pygame.K_DOWN:
                    self.down_arrow = False
                elif event.key == pygame.K_LEFT:
                    self.left_arrow = False
                    self.double_tap_counter = 10
                elif event.key == pygame.K_RIGHT:
                    self.right_arrow = False
                    self.double_tap_counter = 10

        self.events = []

    def uses_event(self, event):
        return event.type == pygame.KEYDOWN or event.type == pygame.KEYUP

    @property
    def shoot(self):
        return self.s_down

    @property
    def ladder_up(self):
        return self.up_arrow

    @property
    def enter_door(self):
        return self.s_down

    @property
    def ladder_down(self):
        return self.down_arrow

    @property
    def left(self):
        return self.left_arrow

    @property
    def right(self):
        return self.right_arrow

    @property
    def jump(self):
        return self.a

    @property
    def double_jump(self):
        return self.up_arrow_down

    @property
    def dash_left(self):
        return self.double_tap_counter > 0 and self.last_arrow_left_or_right == 'left'

    @property
    def dash_right(self):
        return self.double_tap_counter > 0 and self.last_arrow_left_or_right == 'right'

    @property
    def yoyo(self):
        return self.down_arrow

    @property
    def start_up(self):
        return self.up_arrow_down

    @property
    def start_down(self):
        return self.down_arrow_down

    @property
    def start_enter(self):
        return self.a_down

    @property
    def start_back(self):
        return self.s_down
