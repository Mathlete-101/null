from game_object.static.collectible import Collectible


class AnimatedCollectible(Collectible):
    def __init__(self, position, render_target, second_render_target, animation, effect, tags):
        super().__init__(position, render_target, second_render_target, animation.get_frame(0), effect, tags)
        self.animation = animation

    @property
    def image(self):
        return self.animation.render()

    def render(self):
        pass