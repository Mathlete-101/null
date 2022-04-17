import pygame

from controller.controller import Controller

class Key:
    def __init__(self, key, ctrl):
        self.key = key
        self.ctrl = not not ctrl

class FullKeyboardController(Controller):
    def __init__(self):
        super().__init__("full_keyboard_controller")
        self.keys = []
        self.last_key_pressed = ''

    def uses_event(self, event):
        return event.type == pygame.KEYDOWN

    def update(self):
        self.keys = []
        self.last_key_pressed = ''

        for event in self.events:
            if event.type == pygame.KEYDOWN:
                self.keys.append(Key(event.key, event.mod & pygame.KMOD_CTRL))
                if not event.mod & pygame.KMOD_CTRL:
                    self.last_key_pressed = event.unicode

        self.events = []

    def get_key(self, key_, ctrl=None):
        for key in self.keys:
            if key_ == key.key and (ctrl is None or ctrl == key.ctrl):
                return True
        return False



