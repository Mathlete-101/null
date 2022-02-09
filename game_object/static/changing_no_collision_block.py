from game_object.static.changing_block import ChangingBlock
from game_object.static.no_collision_block import NoCollisionBlock


class ChangingNoCollisionBlock(NoCollisionBlock):
    def __init__(self, position, render_target, second_render_target, image):
        super().__init__(position, render_target, image)
        self.second_render_target = second_render_target

    def render(self):
        super().render()
        self.group.draw(self.second_render_target)