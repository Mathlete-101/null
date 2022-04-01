from animation.loop_animation import LoopAnimation
from game_object.static import collectible
from game_object.static.animated_collectible import AnimatedCollectible
from game_object.static.collectible import Collectible
from game_object.static.energy.energy_block import EnergyBlock
from graphics import graphics
from networker.network.energy_network import EnergyNetwork
from tools import duple


class EnergyRechargeBlock(EnergyBlock):
    def __init__(self, position, render_target, second_render_target, network_mgr, graphic):
        super().__init__(position, render_target, network_mgr, graphic)
        self.network = network_mgr.request(self, EnergyNetwork)
        self.tags.append("energy_recharge")
        self.graphic = graphic
        self.switches = [False, False]
        self.render_target = render_target
        self.second_render_target = second_render_target
        self.network_mgr = network_mgr
        self.connection = None
        self.update_ticker = None
        self.power_count = 0
        self.can_emit_energy = False

    def initialize(self):
        self.can_emit_energy = "air" in self.network.level.main[self.location[0]][self.location[1] - 1].tags

    def power_update(self):
        if self.connected and self.connected.supplying:
            self.on()
        else:
            self.off()

    def can_connect(self, location):
        return duple.add(location, (0, -1)) == self.location

    def attempt_connection(self, connector, location):
        if self.can_connect(location):
            self.connected = connector
            return True, self

        return False, None

    def on(self):
        if not self.is_on:
            self.is_on = True
            self.set_image([True, False])
            self.power_count = 0
            self.update_ticker = self.network.update_for(self, 10)

    def deactivate(self):
        if self.is_on:
            self.is_on = False
            self.set_image([False, False])
            self.power_count = 0
            self.update_ticker = None


    def update(self):
        if self.update_ticker.time == 1:
            if self.has_energy:
                self.update_ticker = self.network.update_for(self, 10)

        if not self.currently_has_energy_ball and self.has_energy:
            self.power_count += 1
            self.set_image([True, True])

        if self.power_count == 20:
            if not self.currently_has_energy_ball:
                self.power_count = 0
                self.set_image([True, False])
                self.energy_ball_location = AnimatedCollectible(duple.add(self.location, (0, -1)), self.render_target, self.second_render_target, LoopAnimation(graphics.get("energy_ball"), 2), collectible.get_energy_ball_effect(), ["energy_ball"])
                self.network.level.continuous_block_sprite_group.add(self.energy_ball_location)

    def set_image(self, switches=None):
        if switches is not None:
            self.switches = switches
        self.image = self.graphic.get_sectional(self.switches)
        self.render()

    @property
    def energy_ball_location(self):
        return self.network.level.main[self.location[0]][self.location[1] - 1]

    @energy_ball_location.setter
    def energy_ball_location(self, value):
        self.network.level.main[self.location[0]][self.location[1] - 1] = value

    @property
    def currently_has_energy_ball(self):
        return "energy_ball" in self.energy_ball_location.tags

    @property
    def has_energy(self):
        return self.connected.supplying

    @property
    def supplying(self):
        return False

    @supplying.setter
    def supplying(self, value):
        pass

