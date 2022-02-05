from game_object.static.energy.energy_output_block import EnergyOutputBlock


class EnergyVirtualOutputBlock(EnergyOutputBlock):
    def __init__(self, position, render_target, network_mgr, graphic, parent):
        super().__init__(position, render_target, network_mgr, graphic)
        self.parent = parent

    def render(self):
        pass