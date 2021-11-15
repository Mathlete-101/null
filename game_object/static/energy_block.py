from game_object.static.block import Block


class EnergyBlock(Block):
    def __init__(self, position, render_target, network_mgr, image):
        super().__init__(position, render_target, image)
