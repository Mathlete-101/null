from animation.animation import Animation
from effect.effect import Effect
from game_object.static.energy.energy_receptive_block import EnergyReceptiveBlock
from graphics import graphics
from tools.ticker import Ticker


class EnergyTimedReceptiveBlock(EnergyReceptiveBlock):
    def __init__(self, position, render_target, network_mgr, image):
        super().__init__(position, render_target, network_mgr, image)
        self.tags.append("timed")
        self.on_ticker = Ticker(0)
        self.update_ticker = None

    def on_energy_hit(self, magnitude):
        self.on()
        self.on_ticker.set(60)
        self.network.update_for(self, 60)
        self.supplying = True
        if self.connected:
            self.connected.power_update()
        self.network.level.add_effect(
            Effect(Animation(graphics.get("energy_sphere_decreasing_animation"), 10), self.render_position, True))

    def update(self):
        if self.on_ticker.tick():
            self.supplying = False
            if self.connected:
                self.connected.power_update()
            self.power_update()

    def power_update(self):
        if self.supplying or self.connected and self.connected.is_on:
            self.on()
        else:
            self.off()

