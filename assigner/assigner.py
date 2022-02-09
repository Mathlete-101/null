import math

import graphics.graphics
from game_object.static.block import Block
from game_object.static.data_stick import DataStick
from game_object.static.door_block import DoorBlock
from game_object.static.energy.energy_delay_block import EnergyDelayBlock
from game_object.static.energy.energy_force_field_block import EnergyForceFieldBlock
from game_object.static.energy.energy_timed_receptive_block import EnergyTimedReceptiveBlock
from game_object.static.energy.energy_toggle_receptive_block import EnergyToggleReceptiveBlock
from game_object.static.energy.energy_transistor_block import EnergyTransistorBlock
from game_object.static.energy.energy_wire_block import EnergyWireBlock
from game_object.static.ladder import Ladder
from game_object.static.no_collision_block import NoCollisionBlock
from graphics import graphics
from level.level import Level
from level.level_text import LevelText


# Key

# <space> = air
# B = a standard block/wall/whatever

def assign(level_text: LevelText, level_name):
    level = Level(level_text.dim)

    for i in range(0, level_text.dim[0]):
        for j in range(0, level_text.dim[1]):
            location = (i, j)
            chars = (0 if level_text.background.get(location) == ' ' else level_text.background.get(location),
                     level_text.main.get(location),
                     level_text.foreground.get(location))



            if chars[1] == "B":
                surroundings = level_text.main.get_surrounding_pieces(location)
                edges = [[char != 'B' for char in row] for row in surroundings]

                level.set(location, Block(location, level.world_surface, graphics.get(
                    "platform_" + ("cross" if (location[0] + location[1]) % 2 else "box")).get_with_edge(edges)))

            elif chars[1] == "P":
                level.set(location, DoorBlock(location, level.world_surface, graphics.get("door_" + level_name).get(), level, -1))
                level.set_player_location(location)

            elif chars[1] == "L":
                above_location = (location[0], location[1] - 1)
                obj = Ladder(location, level.world_surface)
                if level_text.main.get(above_location) == " ":
                    obj.is_floor = True
                    obj.is_top_ladder = True
                    obj.image.blit(graphics.get("ladder_platform").get(), (0, 0))
                    obj.render()
                    top = NoCollisionBlock(above_location, level.world_surface, graphics.get("ladder_top").get())
                    level.set(above_location, top)
                    level.block_sprite_group.add(top)
                    level.col_groups[location[0]].add(top)

                level.set(location, obj)

            elif chars[1] == "C":
                level.set(location, NoCollisionBlock(location, level.world_surface, graphics.get("column").get()))

            elif chars[1] == "R":
                level.set(location, EnergyTimedReceptiveBlock(location, level.render_surface, level.network_manager, graphics.get("energy_receiver_time")))

            elif chars[1] == "W":
                level.set(location, EnergyWireBlock(location, level.render_surface, level.network_manager, graphics.get("energy_wire_through")))

            elif chars[1] == "T":
                level.set(location, EnergyToggleReceptiveBlock(location, level.render_surface, level.network_manager, graphics.get("energy_receiver_toggle")))
                if chars[0] == "1":
                    level.main[location[0]][location[1]].supplying = True

            elif chars[1] == "D":
                graphic = graphics.get("energy_delay")
                rotation = int(chars[0])
                graphic = graphic.get_rotation(rotation)
                level.set(location, EnergyDelayBlock(location, level.render_surface, level.network_manager, graphic, rotation))

            elif chars[1] == "t":
                orientation = int(chars[0])
                reflection = bool(orientation % 2)
                rotation = orientation // 2
                graphic = graphics.get("energy_transistor")
                graphic = graphic.get_reflection(reflection)
                graphic = graphic.get_rotation(abs(4 - rotation))
                level.set(location, EnergyTransistorBlock(location, level.render_surface, level.network_manager, graphic, reflection, rotation))

            elif chars[1] == "F":
                level.set(location, EnergyForceFieldBlock(location, level.render_surface, level.network_manager, graphics.get("energy_force_field")))

            elif chars[1] == "d":
                level.set(location, DoorBlock(location, level.world_surface, graphics.get("door_exit").get(), level, 0))

            elif chars[1] in ["1", "2", "3"]:
                block = DataStick(location, level.world_surface, level.render_surface, graphics.get("data_stick_" + chars[1]).get(), 25 * pow(5, int(chars[1])))
                level.set(location, block)
                level.continuous_block_sprite_group.add(block)

            # add the block to the block sprite group and its proper column sprite group
            if len({"air", "data_stick"}.intersection(level.main[location[0]][location[1]].tags)) == 0:
                level.block_sprite_group.add(level.main[location[0]][location[1]])
            level.col_groups[location[0]].add(level.main[location[0]][location[1]])

    return level
