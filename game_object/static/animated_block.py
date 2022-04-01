from animation.animation import Animation
from game_object.static.block import Block
from game_object.static.changing_block import ChangingBlock


class AnimatedBlock(ChangingBlock):
    """A Block whose appearance changes over time."""

    def __init__(self, position, render_target, second_render_target, animation: Animation):
        super().__init__(position, render_target, second_render_target, animation.get_frame(0))
        self.animation = animation

    def render(self):
        self.image = self.animation.render()
        self.group.draw(self.render_target)



