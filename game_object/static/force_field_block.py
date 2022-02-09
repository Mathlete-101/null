import tools.transform
from game_object.static.air import Air
from game_object.static.block import Block


# This is a weird class. If I have to do something like this again, I'm making a metaclass
# It is two blocks squished into one block. If the state is on, it goes to the first block. If it is off, it goes to the second
# AKA State Changing Duple Block
from game_object.static.changing_block import ChangingBlock
from game_object.static.changing_no_collision_block import ChangingNoCollisionBlock
from game_object.static.dirty_block import DirtyBlock
from game_object.static.no_collision_block import NoCollisionBlock


class ForceFieldBlock:
    def __init__(self, position, render_target, second_render_target, image, always_on_group, column_group):
        super().__setattr__("on", False)
        super().__setattr__("force_field_block", Block(position, render_target, image))
        super().__setattr__("air_block", NoCollisionBlock(position, render_target, tools.transform.get_white_surface((42, 42))))
        super().__setattr__("second_render_target", second_render_target)
        super().__setattr__("always_on_group", always_on_group)
        column_group.add(self.air_block, self.force_field_block)

    def __getattribute__(self, item):
        if item in ["air_block", "force_field_block", "on", "second_render_target", "always_on_group"]:
            return super().__getattribute__(item)
        elif self.on:
            return self.force_field_block.__getattribute__(item)
        else:
            return self.air_block.__getattribute__(item)

    def __setattr__(self, key, value):
        if key in ["air_block", "force_field_block", "on", "second_render_target", "always_on_group"]:
            super().__setattr__(key, value)
            if key == "on":
                self.render()
                if value:
                    self.force_field_block.add(self.always_on_group)
                else:
                    self.force_field_block.remove(self.always_on_group)
                    self.force_field_block.group.clear(self.force_field_block.render_target, self.second_render_target)
        elif self.on:
            self.force_field_block.__setattr__(key, value)
        else:
            self.air_block.__setattr__(key, value)
