from game_object.static.energy.energy_block import EnergyBlock
from graphics.graphic_class.rotation_reflection_sectional_switch_graphic import RotationReflectionSectionalSwitchGraphic
from misc.energy_connection_tracker import EnergyConnectionTracker
from misc.virtual_energy_connection.virtual_energy_input import VirtualEnergyInput
from misc.virtual_energy_connection.virtual_energy_output import VirtualEnergyOutput
from networker.network.energy_network import EnergyNetwork


class EnergyTransistorBlock(EnergyBlock):
    def __init__(self, position, render_target, network_mgr, graphic: RotationReflectionSectionalSwitchGraphic, reflection, rotation):
        super().__init__(position, render_target, network_mgr, graphic)
        self.tags.append("transistor")
        self.network = network_mgr.request(self, EnergyNetwork)
        self.connection_tracker = EnergyConnectionTracker(True, True, False, True, self.location, reflection=reflection, rotation=rotation)
        self.storage = [False, False]
        self.alpha_input = None
        self.beta_input = None
        self.output = None
        self.power_update()
        self.render()

    def can_connect(self, location):
        return self.connection_tracker.check(location, False)[0]

    def attempt_connection(self, connector, location):
        check, orientation = self.connection_tracker.check(location, True)
        if check:
            if orientation == 1:
                self.alpha_input = VirtualEnergyInput(self, orientation)
                self.alpha_input.connected = connector
                return True, self.alpha_input
            elif orientation == 0:
                self.beta_input = VirtualEnergyInput(self, orientation)
                self.beta_input.connected = connector
                return True, self.beta_input
            elif orientation == 3:
                self.output = VirtualEnergyOutput(self, orientation)
                self.output.connected = connector
                return True, self.output
        return False, None

    def set_powered(self, orientation, powered):
        self.storage[orientation] = powered
        self.power_update()

    def power_update(self):
        display = [self.storage[1],
                   self.storage[0] != self.storage[1],
                   self.storage[1] and not self.storage[0],
                   self.storage[0],
                   self.storage[0] and self.storage[1]]

        self.image = self.graphic.get_sectional(display)
        self.render()

        if self.output:
            self.output.supplying = self.storage[1] and not self.storage[0]


