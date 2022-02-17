from game_object.static.energy.energy_wire_block import EnergyWireBlock
from game_object.static.no_collision_block import NoCollisionBlock


class EnergyWireNoCollisionBlock(EnergyWireBlock, NoCollisionBlock):
    """An energy wire that connects to other wires but the player is able to walk through."""

    def __init__(self, position, render_target, network_mgr, image):
        super().__init__(position, render_target, network_mgr, image)
        self.tags.append("dark")
