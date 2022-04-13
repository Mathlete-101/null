from game_object.static.no_collision_block import NoCollisionBlock
from sound import sounds


class DoorBlock(NoCollisionBlock):
    def __init__(self, position, render_target, image, level, trigger_code):
        super().__init__(position, render_target, image)
        self.tags.append("door")
        self.trigger_code = trigger_code
        self.level = level

    def enter(self, player):
        if self.trigger_code != -1:
            sounds.play_sound("door")
            self.level.complete_level(player)
