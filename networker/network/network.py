import tools.duple
from tools import duple


class Network:
    def __init__(self, obj):
        self.objects = [obj]
        self.network_type = "none"

    def __len__(self):
        return len(self.objects)

    def add_obj(self, obj):
        self.objects.append(obj)

    def merge(self, network):
        self.objects = self.objects + network.objects

    def update(self):
        pass

    def get_locations(self):
        return [obj.location for obj in self.objects]

    def touches(self, network):
        for obj in network.objects:
            for self_obj in self.objects:
                if duple.adjacent(obj, self_obj):
                    return True
        return False

    def initialize(self):
        pass
