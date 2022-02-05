import tools.duple
from tools import duple


class Network:
    def __init__(self, obj, level):
        self.objects = [obj]
        self.level = level
        self.network_type = "none"

    def __len__(self):
        return len(self.objects)

    def add_obj(self, obj):
        self.objects.append(obj)

    def merge(self, network):
        for obj in network.objects:
            obj.network = self
        self.objects = self.objects + network.objects

    def update(self):
        pass

    def get_locations(self):
        return [obj.location for obj in self.objects]

    def touches(self, network):
        for obj in network.objects:
            if self.touches_block(obj):
                return True
        return False

    def touches_block(self, block):
        for self_obj in self.objects:
            if duple.adjacent(block.location, self_obj.location):
                return True
        return False

    def initialize(self):
        pass

    def alert(self):
        for obj in self.objects:
            obj.alert()
