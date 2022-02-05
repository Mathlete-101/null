from graphics.graphic_class.graphic import Graphic


class AnimationGraphic(Graphic):
    def __len__(self):
        return len(self.img)

    def get_all(self):
        return self.img
