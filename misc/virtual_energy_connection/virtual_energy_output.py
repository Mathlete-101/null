from misc.virtual_energy_connection.virtual_energy_connection import VirtualEnergyConnection


class VirtualEnergyOutput(VirtualEnergyConnection):

    @property
    def supplying(self):
        return self._supplying

    @supplying.setter
    def supplying(self, val):
        print(val, self.connected)
        self._supplying = val
        if self.connected:
            self.connected.power_update()

    def power_update(self):
        pass
