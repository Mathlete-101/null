from game_object.static.energy.energy_block import EnergyBlock
from game_object.static.force_field_block import ForceFieldBlock
from networker.network.energy_network import EnergyNetwork
from tools import duple
from graphics import graphics


class EnergyForceFieldBlock(EnergyBlock):
    def __init__(self, position, render_target, network_mgr, graphic):
        super().__init__(position, render_target, network_mgr, graphic)
        self.network = network_mgr.request(self, EnergyNetwork)
        self.connected = None
        self.tags.append("force_field")
        self.orientation = (0, 0)
        self.force_fields = []

    def power_update(self):
        if self.connected and self.connected.supplying:
            self.on()
        else:
            self.off()
        for f in self.force_fields:
            f.on = self.connected.supplying

    def attempt_connection(self, connector, location):
        if self.can_connect(None):
            self.connected = connector
            return True, self
        return False, None

    def can_connect(self, location):
        return self.connected is None

    def initialize(self):
        if self.orientation != (0, 0):
            print(self.orientation)
            position = duple.add(self.location, self.orientation)
            while "air" in self.network.level.main[position[0]][position[1]].tags:
                graphic = graphics.get("force_field").get_rotation(0 if self.orientation[0] else 90)
                new_block = ForceFieldBlock(position, self.render_target, self.network.level.world_surface, graphic, self.network.level.continuous_block_sprite_group, self.network.level.col_groups[position[0]])
                self.network.level.main[position[0]][position[1]] = new_block
                self.force_fields.append(new_block)
                position = duple.add(position, self.orientation)

        self.power_update()

