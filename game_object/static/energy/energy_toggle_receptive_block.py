from animation.loop_switchable_animation import LoopSwitchableAnimation
from effect.effect import Effect
from game_object.static.energy.energy_receptive_block import EnergyReceptiveBlock
from graphics import graphics


class EnergyToggleReceptiveBlock(EnergyReceptiveBlock):
    def __init__(self, position, render_target, network_mgr, image, start_on = False):
        super().__init__(position, render_target, network_mgr, image)
        self.tags.append("toggle")
        if start_on:
            self.on()
            self.supplying = True
        self.supplying = False
        self.energy_ball = LoopSwitchableAnimation(graphics.get("energy_sphere_static_animation"))
        self.energy_ball.on = False
        self.network.level.add_effect(Effect(self.energy_ball, self.render_position, True))

    def on_energy_hit(self, magnitude):
        self.supplying = not self.supplying
        self.energy_ball.on = not self.energy_ball.on
        self.connected.power_update()

    def off(self):
        super().off()
        self.energy_ball.on = False

    def initialize(self):
        if self.supplying:
            self.energy_ball.on = not self.energy_ball.on
            self.connected.power_update()
            self.render()

    def update(self):
        super().update()

    def power_update(self):
        if self.supplying or self.connected and self.connected.supplying:
            self.on()
        else:
            self.off()