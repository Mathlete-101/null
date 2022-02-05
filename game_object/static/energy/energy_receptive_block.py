from game_object.static.energy.energy_output_block import EnergyOutputBlock
from networker.network.energy_network import EnergyNetwork


class EnergyReceptiveBlock(EnergyOutputBlock):

    def __init__(self, position, render_target, network_mgr, image):
        super().__init__(position, render_target, network_mgr, image)
        self.tags.append("energy_receptive")
        self.network = network_mgr.request(self, EnergyNetwork)
        self.connected = None

    def on_energy_hit(self, magnitude):
        pass

    def update(self):
        pass

    def power_update(self):
        pass

    def attempt_connection(self, connector, location):
        if self.connected is None:
            self.connected = connector
            return True, self
        return False, None

    def can_connect(self, location):
        return self.connected is None


