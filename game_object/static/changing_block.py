from game_object.static.block import Block


class ChangingBlock(Block):
    def __init__(self, position, render_target, second_render_target, image):
        super().__init__(position, render_target, image)
        self.second_render_target = second_render_target

    def render(self):
        super().render()
        self.group.draw(self.second_render_target)