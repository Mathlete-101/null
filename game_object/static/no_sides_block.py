from game_object.static.block import Block


# never implement this class. It will cause problems if you do
class NoSidesBlock(Block):
    def __init__(self, position, render_target, image):
        super().__init__(position, render_target, image)
        self.is_floor = False
        self.is_ceiling = False
        self.is_left_wall = False
        self.is_right_wall = False
