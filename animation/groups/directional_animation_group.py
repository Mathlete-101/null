from animation.animation import Animation
from animation.directional_animation import DirectionalAnimation
from animation.groups.animation_group import AnimationGroup


class DirectionalAnimationGroup(AnimationGroup):
    def add(self, animation: DirectionalAnimation):
        super().add(animation)

    def set_left(self, left):
        for animation in self.animations:
            animation.set_left(left)
