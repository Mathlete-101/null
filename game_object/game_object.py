class GameObject:
    def __init__(self, location: (int, int)):
        self.location = location
        self.tags = []

    @property
    def x(self):
        return self.location[0]

    @x.setter
    def x(self, val):
        self.location = (val, self.location[1])

    @property
    def y(self):
        return self.location[1]

    @y.setter
    def y(self, val):
        self.location = (self.location[0], val)
