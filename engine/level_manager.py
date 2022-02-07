

class LevelManager:
    def __init__(self, levels):
        self.levels = levels
        self.current_level = 0

    def get_current_level(self):
        return self.levels[self.current_level]

    def next_level(self):
        self.levels[self.current_level] = None
        self.levels += 1



