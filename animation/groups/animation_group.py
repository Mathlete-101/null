from animation.animation import Animation


class AnimationGroup:
    def __init__(self):
        self.animations: list(Animation) = []

    def add(self, animation: Animation):
        self.animations.append(animation)
