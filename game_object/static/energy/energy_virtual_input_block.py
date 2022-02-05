from game_object.static.energy.energy_block import EnergyBlock


class EnergyVirtualInputBlock(EnergyBlock):
    def power_update(self):
        self.parent.set_powered(self.direction, self.connected and self.connected.supplying)

    def __init__(self, position, render_target, network_mgr, graphic, parent, direction):
        super().__init__(position, render_target, network_mgr, graphic)
        self.parent = parent
        self.direction = direction

    def render(self):
        pass
