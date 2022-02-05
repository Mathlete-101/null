from graphics.graphic_class.graphic import Graphic


class SwitchGraphic(Graphic):
    def __init__(self, off, on):
        super().__init__(off)
        self.off = off
        self.on = on

    def get_on(self):
        return self.on

    def get_off(self):
        return self.off

    def get_all(self):
        return [self.on, self.off]
