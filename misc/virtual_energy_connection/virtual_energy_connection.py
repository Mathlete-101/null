class VirtualEnergyConnection():

    def __init__(self, parent, direction):
        self.connected = None
        self.parent = parent
        self.direction = direction
        self.supplying = False
