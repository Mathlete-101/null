import tools.transform
from animation.animation import Animation
from graphics.graphic_class.graphic import Graphic


class SwitchableAnimation(Animation):

    def render(self):
        r = super().render()
        if self.on:
            return r
        else:
            return self.clear_surface

    def __init__(self, graphic: Graphic, slowness=1):
        super().__init__(graphic, slowness)
        self.on = False
        self.clear_surface = tools.transform.get_clear_surface((42, 42))
