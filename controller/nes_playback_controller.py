import json

from controller.nes_controller import NESController


class NESPlaybackController(NESController):

    def __init__(self, controller_id):
        super().__init__(controller_id)
        self.recording = []

    def uses_event(self, event):
        return False

    def update(self):
        if len(self.recording) > 0:
            # controllers could clearly be better, but I don't have time to fix it
            frame = self.recording.pop(0)
            self.a_button = "a_button" in frame
            self.a_button_down = "a_button_down" in frame
            self.b_button = "b_button" in frame
            self.b_button_down = "b_button_down" in frame
            self.up_dpad = "up_dpad" in frame
            self.up_dpad_down = "up_dpad_down" in frame
            self.down_dpad = "down_dpad" in frame
            self.down_dpad_down = "down_dpad_down" in frame
            self.left_dpad = "left_dpad" in frame
            self.left_dpad_down = "left_dpad_down" in frame
            self.left_dpad_double_click = "left_dpad_double_click" in frame
            self.right_dpad = "right_dpad" in frame
            self.right_dpad_down = "right_dpad_down" in frame
            self.right_dpad_double_click = "right_dpad_double_click" in frame
            self.select_button = "select_button" in frame
            self.select_button_down = "select_button_down" in frame
            self.start_button = "start_button" in frame
            self.start_button_down = "start_button_down" in frame
        else:
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

    def load(self, file_path):
        """Load recording from json file"""
        with open(file_path, "r") as f:
            self.recording = json.load(f)

