from misc.virtual_energy_connection.virtual_energy_connection import VirtualEnergyConnection


class VirtualEnergyInput(VirtualEnergyConnection):

    def power_update(self):
        self.parent.set_powered(self.direction, self.connected and self.connected.supplying)
