from animation.animation import Animation
from graphics.graphic_class.graphic import Graphic


class DirectionalAnimation(Animation):

    def __init__(self, graphic: Graphic, slowness=1):
        super().__init__(graphic, slowness)
        self.left = True

    @property
    def dim(self):
        return self.graphic.get()[0][0].get_size()

    def set_left(self, left):
        self.left = left

    def get_frame(self, position):
        return self.graphic.get()[position][0 if self.left else 1]
