import functools

from game_object.static.energy.energy_block import EnergyBlock
from misc.energy_connection_tracker import EnergyConnectionTracker
from misc.virtual_energy_connection.virtual_energy_input import VirtualEnergyInput
from misc.virtual_energy_connection.virtual_energy_output import VirtualEnergyOutput
from networker.network.energy_network import EnergyNetwork


class EnergyDelayBlock(EnergyBlock):
    def __init__(self, position, render_target, network_mgr, graphic, rotation):
        super().__init__(position, render_target, network_mgr, graphic)
        self.network = network_mgr.request(self, EnergyNetwork)
        self.storage = [False, False, False, False, False]
        self.tags.append("delay")
        self.rotation = rotation
        self.connection_tracker = EnergyConnectionTracker(True, False, True, False, self.location, rotation=rotation)
        self.input_connection = None
        self.output_connection = None
        self.update_ticker = None
        self.set_image()

    def attempt_connection(self, connector, location):
        check, orientation = self.connection_tracker.check(location, True)
        if check:
            if orientation == 2:
                self.input_connection = VirtualEnergyInput(self, orientation)
                self.input_connection.connected = connector
                return True, self.input_connection
            elif orientation == 0:
                self.output_connection = VirtualEnergyOutput(self, orientation)
                self.output_connection.connected = connector
                return True, self.output_connection
        return False, None

    def can_connect(self, location):
        return self.connection_tracker.check(location, False)

    def on(self):
        self.is_on = True

    def off(self):
        self.is_on = False

    def set_powered(self, orientation, powered):
        if powered:
            self.update_ticker = self.network.update_for(self, 11)
            self.on()
        else:
            self.off()

    def update(self):
        if self.update_ticker.time == 1:
            if self.has_energy:
                self.update_ticker.time = 11
            self.storage = [self.is_on] + self.storage
            self.supplying = self.storage.pop()
            self.set_image()
            self.render()

    def set_image(self):
        self.image = self.graphic.get_sectional([self.is_on] + self.storage + [self.supplying])


    @property
    def has_energy(self):
        return functools.reduce(lambda a, b: a or b, self.storage) or self.is_on

    @property
    def supplying(self):
        return self.output_connection.supplying if self.output_connection else False

    @supplying.setter
    def supplying(self, val):
        self.output_connection.supplying = val

