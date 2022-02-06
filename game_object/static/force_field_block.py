import tools.transform
from game_object.static.air import Air
from game_object.static.block import Block


# This is a weird class. If I have to do something like this again, I'm making a metaclass
# It is two blocks squished into one block. If the state is on, it goes to the first block. If it is off, it goes to the second
# AKA State Changing Duple Block
from game_object.static.no_collision_block import NoCollisionBlock


class ForceFieldBlock:
    def __init__(self, position, render_target, image):
        super().__setattr__("on", False)
        super().__setattr__("force_field_block", Block(position, render_target, image))
        super().__setattr__("air_block", NoCollisionBlock(position, render_target, tools.transform.get_white_surface((21, 21))))
        self.air_block.image = tools.transform.get_white_surface((21, 21))

    def __getattribute__(self, item):
        if item in ["air_block", "force_field_block", "on"]:
            return super().__getattribute__(item)
        elif self.on:
            return self.force_field_block.__getattribute__(item)
        else:
            return self.air_block.__getattribute__(item)

    def __setattr__(self, key, value):
        if key in ["air_block", "force_field_block", "on"]:
            super().__setattr__(key, value)
            if key == "on":
                self.render()
        elif self.on:
            self.force_field_block.__setattr__(key, value)
        else:
            self.air_block.__setattr__(key, value)
