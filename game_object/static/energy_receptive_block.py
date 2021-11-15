from game_object.static.energy_block import EnergyBlock


class EnergyReceptiveBlock(EnergyBlock):

    def __init__(self, position, render_target, network_mgr, image):
        super().__init__(position, render_target, network_mgr, image)
        self.tags.append("energy_receptive")
        self.network = network_mgr.request(self, "energy")

    def on_energy_hit(self, magnitude):
        self.network.laser(magnitude, self)