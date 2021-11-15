from game_object.static.no_sides_block import NoSidesBlock


# if you want an object that looks but doesn't hit, use this
class NoCollisionBlock(NoSidesBlock):
    def check_support(self, hitbox):
        return False

    def __init__(self, position, render_target, image):
        super().__init__(position, render_target, image)
        self.opaque = False
