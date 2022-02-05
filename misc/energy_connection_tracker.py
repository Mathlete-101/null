from tools import duple


class EnergyConnectionTracker:
    def rotate(self):
        up = self.up
        self.up = self.right
        self.right = self.down
        self.down = self.left
        self.left = up

    def reflect(self):
        up = self.up
        self.up = self.down
        self.down = up

    def __init__(self, up, left, down, right, location, rotation=0, reflection=False):
        self.up = (0, up)
        self.left = (1, left)
        self.down = (2, down)
        self.right = (3, right)
        if reflection:
            self.reflect()
        while rotation > 0:
            self.rotate()
            rotation -= 1
        self.location = location

    def check(self, location, fill):
        difference = duple.subtract(self.location, location)
        print(difference[0])
        fill = not fill
        if difference[1] == -1:
            if self.up[1]:
                self.up = duple.insert(self.up, fill)
                return True, self.up[0]
            return False, self.up[0]
        elif difference[1] == 1:
            if self.down[1]:
                self.down = duple.insert(self.down, fill)
                return True, self.down[0]
            return False, self.down[0]
        elif difference[0] == -1:
            if self.right[1]:
                self.right = duple.insert(self.right, fill)
                return True, self.right[0]
            return False, self.right[0]
        else:
            if self.left[1]:
                self.left = duple.insert(self.left, fill)
                return True, self.left[0]
            return False, self.left[0]
