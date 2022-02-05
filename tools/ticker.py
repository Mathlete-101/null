class Ticker:
    def __init__(self, length):
        self.time = length

    def tick(self):
        self.time -= 1
        return self.time <= 0

    def set(self, time):
        self.time = time
