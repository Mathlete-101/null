from animation.loop_animation import LoopAnimation
from animation.switchable_animation import SwitchableAnimation
from graphics.graphic_class.graphic import Graphic


class LoopSwitchableAnimation(SwitchableAnimation, LoopAnimation):

    def __init__(self, graphic: Graphic, slowness=1):
        super().__init__(graphic, slowness)
