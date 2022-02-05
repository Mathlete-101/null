from game_object.static.energy.energy_block import EnergyBlock
from networker.network.energy_network import EnergyNetwork


class EnergyWireBlock(EnergyBlock):
    def __init__(self, position, render_target, network_mgr, image):
        super().__init__(position, render_target, network_mgr, image)
        self.network = network_mgr.request(self, EnergyNetwork)
        self.on_img = image
        self.off_img = image
        self.tags.append("wire")

