from game_object.static.block import Block


class LaserThroughBlock(Block):
    @property
    def opaque(self):
        return False
