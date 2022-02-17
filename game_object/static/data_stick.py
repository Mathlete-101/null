import tools.transform
from game_object.static.air import Air
from game_object.static.no_sides_block import NoSidesBlock


class DataStick (NoSidesBlock):
    def __init__(self, position, render_target, second_render_target, image, value):
        super().__init__(position, render_target, image)
        self.value = value
        self.second_render_target = second_render_target
        self.tags.append("data_stick")
        self.opaque = False
        self.is_floor = False

    def collect(self):
        from engine.game import engine

        # yay points
        engine.score += self.value

        # seppuku
        self.group.clear(self.render_target, self.second_render_target)
        engine.current_level.main[self.location[0]][self.location[1]] = Air(self.location)
        self.kill()

    def check_support(self, hitbox):
        return False


