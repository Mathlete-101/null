from graphics.graphic_class.animation_graphic import AnimationGraphic


class HiddenAnimationGraphic(AnimationGraphic):
    """Basically just an animation pretending to be a graphic"""

    def __init__(self, images):
        super().__init__(images)
        self.place_at = 0

    def get(self):
        if self.place_at == len(self):
            self.place_at = 0
        return self.get_all()[self.place_at]

    def copy(self):
        return HiddenAnimationGraphic(self.get_all())
