import json

from controller.nes_controller import NESController


class NESRecorderController(NESController):
    def __init__(self, controller_id):
        super().__init__(controller_id)
        self.recording = []

    def update(self):
        super().update()
        self.record_input()

    def record_input(self):
        """

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
        """
        buttons_currently_pressed = []
        if self.a_button:
            buttons_currently_pressed.append('a_button')
        if self.a_button_down:
            buttons_currently_pressed.append('a_button_down')
        if self.b_button:
            buttons_currently_pressed.append('b_button')
        if self.b_button_down:
            buttons_currently_pressed.append('b_button_down')
        if self.up_dpad:
            buttons_currently_pressed.append('up_dpad')
        if self.up_dpad_down:
            buttons_currently_pressed.append('up_dpad_down')
        if self.down_dpad:
            buttons_currently_pressed.append('down_dpad')
        if self.down_dpad_down:
            buttons_currently_pressed.append('down_dpad_down')
        if self.left_dpad:
            buttons_currently_pressed.append('left_dpad')
        if self.left_dpad_down:
            buttons_currently_pressed.append('left_dpad_down')
        if self.left_dpad_double_click:
            buttons_currently_pressed.append('left_dpad_double_click')
        if self.right_dpad:
            buttons_currently_pressed.append('right_dpad')
        if self.right_dpad_down:
            buttons_currently_pressed.append('right_dpad_down')
        if self.right_dpad_double_click:
            buttons_currently_pressed.append('right_dpad_double_click')
        if self.select_button:
            buttons_currently_pressed.append('select_button')
        if self.select_button_down:
            buttons_currently_pressed.append('select_button_down')
        if self.start_button:
            buttons_currently_pressed.append('start_button')
        if self.start_button_down:
            buttons_currently_pressed.append('start_button_down')

        self.recording.append(buttons_currently_pressed)


    def save(self, file_path):
        """JSON dump the recording to a file"""
        with open(file_path, 'w') as f:
            f.write(json.dumps(self.recording))
        self.recording = []

    def reset_recording(self):
        self.recording = []

