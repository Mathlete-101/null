import tools.transform
from game_object.static.air import Air
from game_object.static.no_sides_block import NoSidesBlock


class Collectible (NoSidesBlock):
    def __init__(self, position, render_target, second_render_target, image, effect, tags):
        super().__init__(position, render_target, image)
        self.second_render_target = second_render_target
        self.tags.append("collectible")
        self.tags += tags
        self.effect = effect
        self.is_floor = False
        self.has_been_collected = False

    @property
    def opaque(self):
        return False

    def collect(self, player):
        from engine.game import engine

        # yay effect
        self.effect(player)

        # seppuku
        self.group.clear(self.render_target, self.second_render_target)
        self.has_been_collected = True
        engine.current_level.main[self.location[0]][self.location[1]] = Air(self.location)
        self.kill()

    def check_support(self, hitbox):
        return False


def get_data_stick_effect(value):
    def func(player):
        from engine.game import engine
        engine.score += value
    return func


# This function returns a function for consistency
def get_movement_belt_effect():
    def func(player):
        player.movement_belt = True
    return func

def get_energy_ball_effect():
    def func(player):
        player.movement_belt_charges = 3
    return func
