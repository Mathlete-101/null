from game_object.static.energy.energy_block import EnergyBlock


class EnergyOutputBlock(EnergyBlock):
    def __init__(self, position, render_target, network_mgr, graphic):
        super().__init__(position, render_target, network_mgr, graphic)
        self.supplying = False


