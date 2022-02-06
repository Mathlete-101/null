from game_object.static.block import Block


class EnergyBlock(Block):
    @property
    def graphic(self):
        return self._graphic

    @graphic.setter
    def graphic(self, graphic):
        self._graphic = graphic
        if self.is_on:
            self.image = self.graphic.get_on()
        else:
            self.image = self.graphic.get_off()
        self.render()

    def __init__(self, position, render_target, network_mgr, graphic):
        super().__init__(position, render_target, graphic.get())
        self.is_on = False
        self.graphic = graphic
        self.tags.append("energy")
        self.supplying = False

    def on(self):
        self.image = self.graphic.get_on()
        self.render()
        self.is_on = True

    def off(self):
        self.image = self.graphic.get_off()
        self.render()
        self.is_on = False

    def power_update(self):
        self.off()

    def attempt_connection(self, connector, location):
        return False, None

    def can_connect(self, location):
        return False

    def initialize(self):
        pass
