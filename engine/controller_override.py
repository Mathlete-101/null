class ControllerStep:
    def __init__(self, function, frames):
        self.function = function
        self.frames = frames

class ControllerOverride:
    def __init__(self, steps):
        self.steps = steps
        self.current_step = 0
        self.current_frame = 0

    def run(self):
        if self.current_frame >= self.steps[self.current_step].frames:
            self.current_step += 1
            self.current_frame = 0
        if self.current_step >= len(self.steps):
            return
        self.steps[self.current_step].function()
        self.current_frame += 1

    def reset(self):
        self.current_step = 0
        self.current_frame = 0

    def is_complete(self):
        return self.current_step >= len(self.steps)
