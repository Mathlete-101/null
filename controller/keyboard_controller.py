import pygame

from controller.controller import Controller


STANDARD_LAYOUT = {
    "a": pygame.K_a,
    "s": pygame.K_s,
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT
}

LEFT_SIDE_LAYOUT = {
    "a": pygame.K_BACKQUOTE,
    "s": pygame.K_1,
    "up": pygame.K_w,
    "down": pygame.K_s,
    "left": pygame.K_a,
    "right": pygame.K_d
}

RIGHT_SIDE_LAYOUT = {
    "a": pygame.K_COMMA,
    "s": pygame.K_PERIOD,
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT
}


class KeyboardController(Controller):

    def __init__(self, keyboard_controller_layout=None, controller_type="keyboard"):
        super().__init__(controller_type)
        if keyboard_controller_layout is None:
            keyboard_controller_layout = STANDARD_LAYOUT
        self.keyboard_controller_layout = keyboard_controller_layout

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
                if event.key == self.keyboard_controller_layout["a"]:
                    self.a = True
                    self.a_down = True
                elif event.key == self.keyboard_controller_layout["s"]:
                    self.s = True
                    self.s_down = True
                elif event.key == self.keyboard_controller_layout["up"]:
                    self.up_arrow = True
                    self.up_arrow_down = True
                elif event.key == self.keyboard_controller_layout["down"]:
                    self.down_arrow = True
                    self.down_arrow_down = True
                elif event.key == self.keyboard_controller_layout["left"]:
                    self.left_arrow = True
                    self.left_arrow_down = True
                    self.last_arrow_left_or_right = 'left'
                elif event.key == self.keyboard_controller_layout["right"]:
                    self.right_arrow = True
                    self.right_arrow_down = True
                    self.last_arrow_left_or_right = 'right'
            elif event.type == pygame.KEYUP:
                if event.key == self.keyboard_controller_layout["a"]:
                    self.a = False
                elif event.key == self.keyboard_controller_layout["s"]:
                    self.s = False
                elif event.key == self.keyboard_controller_layout["up"]:
                    self.up_arrow = False
                elif event.key == self.keyboard_controller_layout["down"]:
                    self.down_arrow = False
                elif event.key == self.keyboard_controller_layout["left"]:
                    self.left_arrow = False
                    self.double_tap_counter = 10
                elif event.key == self.keyboard_controller_layout["right"]:
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

    @property
    def start_left(self):
        return self.left_arrow_down

    @property
    def start_right(self):
        return self.right_arrow_down

    def clear(self):
        self.a = False
        self.s = False
        self.up_arrow = False
        self.down_arrow = False
        self.left_arrow = False
        self.right_arrow = False
        self.double_tap_counter = 0
        self.last_arrow_left_or_right = None
        self.up_arrow_down = False
        self.down_arrow_down = False
        self.left_arrow_down = False
        self.right_arrow_down = False
        self.s_down = False
        self.a_down = False

    def clear_movement_belt(self):
        self.double_tap_counter = 0
        self.last_arrow_left_or_right = None
        self.down_arrow_down = False
        self.a_down = False

