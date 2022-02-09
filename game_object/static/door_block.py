from game_object.static.no_collision_block import NoCollisionBlock
from level.level import Level

class DoorBlock(NoCollisionBlock):
    def __init__(self, position, render_target, image, level, trigger_code):
        super().__init__(position, render_target, image)
        self.tags.append("door")
        self.trigger_code = trigger_code
        self.level = level

    def enter(self):
        if self.trigger_code != -1:
            from engine.engine import engine
            engine.score += (1 + self.trigger_code) * 1000
            engine.next_level()
            self.trigger_code = -1
