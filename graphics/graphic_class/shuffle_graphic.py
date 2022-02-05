from graphics.graphic_class.graphic import Graphic
from tools import lists


class ShuffleGraphic(Graphic):
    def get(self):
        return lists.choose(self.img)

    def get_all(self):
        return self.img