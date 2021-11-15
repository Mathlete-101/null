from animation.animation import Animation


class LoopAnimation(Animation):
    def increment(self):
        self.position += 1
        self.position %= self.length

    @property
    def ended(self):
        return False
