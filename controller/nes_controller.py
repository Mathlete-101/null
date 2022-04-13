from controller.controller import Controller
import pygame


class NESController(Controller):
    """
    A USB NES Controller
    Should override all @property methods of the Controller class.
    A: jump
    B: shoot
    up: ladder up
    down: yoyo, ladder down
    left: go to the left
    double click left: dash to the left
    right: go to the right
    double click right: dash to the right
    """
    def __init__(self, joystick_id):
        Controller.__init__(self)
        self.joystick_id = joystick_id

        self.a_button = False
        self.a_button_down = False
        self.b_button = False
        self.b_button_down = False
        self.up_dpad = False
        self.up_dpad_down = False
        self.down_dpad = False
        self.down_dpad_down = False
        self.left_dpad = False
        self.left_dpad_down = False
        self.left_dpad_double_click = False
        self.right_dpad = False
        self.right_dpad_down = False
        self.right_dpad_double_click = False
        self.select_button = False
        self.select_button_down = False
        self.start_button = False
        self.start_button_down = False

        self.dpad_threshold = 0.2

        self.double_click_counter = 0
        self.last_direction_left_or_right = ''
        self.double_click_threshold = 10

    def update(self):
        # update double click counter
        if self.double_click_counter > 0:
            self.double_click_counter -= 1

        # reset variables ending in _down to False
        self.a_button_down = False
        self.b_button_down = False
        self.up_dpad_down = False
        self.down_dpad_down = False
        self.left_dpad_down = False
        self.right_dpad_down = False
        self.select_button_down = False
        self.start_button_down = False

        self.left_dpad_double_click = False
        self.right_dpad_double_click = False

        # update buttons
        # a button is 1
        # b button is 2

        for event in self.events:
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 1:
                    self.a_button_down = True
                    self.a_button = True
                elif event.button == 2:
                    self.b_button_down = True
                    self.b_button = True
                elif event.button == 8:
                    self.select_button_down = True
                    self.select_button = True
                elif event.button == 9:
                    self.start_button_down = True
                    self.start_button = True
            elif event.type == pygame.JOYBUTTONUP:
                if event.button == 1:
                    self.a_button_down = False
                    self.a_button = False
                elif event.button == 2:
                    self.b_button_down = False
                    self.b_button = False
                elif event.button == 8:
                    self.select_button_down = False
                    self.select_button = False
                elif event.button == 9:
                    self.start_button_down = False
                    self.start_button = False
            elif event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    if event.value < -self.dpad_threshold:
                        if not self.left_dpad:
                            self.left_dpad_down = True
                            if self.last_direction_left_or_right == 'left' and self.double_click_counter > 0:
                                self.left_dpad_double_click = True
                            self.last_direction_left_or_right = 'left'
                            self.double_click_counter = self.double_click_threshold
                        self.left_dpad = True
                    elif event.value > self.dpad_threshold:
                        if not self.right_dpad:
                            self.right_dpad_down = True
                            if self.last_direction_left_or_right == 'right' and self.double_click_counter > 0:
                                self.right_dpad_double_click = True
                            self.last_direction_left_or_right = 'right'
                            self.double_click_counter = self.double_click_threshold
                        self.right_dpad = True
                    else:
                        self.left_dpad = False
                        self.right_dpad = False
                elif event.axis == 4:
                    if event.value < -self.dpad_threshold:
                        if not self.up_dpad:
                            self.up_dpad_down = True
                        self.up_dpad = True
                    elif event.value > self.dpad_threshold:
                        if not self.down_dpad:
                            self.down_dpad_down = True
                        self.down_dpad = True
                    else:
                        self.up_dpad = False
                        self.down_dpad = False

        self.events = []


    def uses_event(self, event):
        return (event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP or event.type == pygame.JOYAXISMOTION) and event.joy == self.joystick_id

    @property
    def shoot(self):
        return self.b_button

    @property
    def ladder_up(self):
        return self.up_dpad

    @property
    def ladder_down(self):
        return self.down_dpad

    @property
    def left(self):
        return self.left_dpad

    @property
    def right(self):
        return self.right_dpad

    @property
    def jump(self):
        return self.a_button

    @property
    def double_jump(self):
        return self.a_button_down

    @property
    def dash_left(self):
        return self.left_dpad_double_click

    @property
    def dash_right(self):
        return self.right_dpad_double_click

    @property
    def yoyo(self):
        return self.down_dpad_down

    @property
    def start_up(self):
        return self.up_dpad_down

    @property
    def start_down(self):
        return self.down_dpad_down or self.select_button_down

    @property
    def start_enter(self):
        return self.start_button_down or self.a_button_down

    @property
    def enter_door(self):
        return self.b_button_down

    @property
    def start_back(self):
        return self.b_button_down
