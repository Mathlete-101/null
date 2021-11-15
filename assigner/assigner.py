import graphics.graphics
from game_object.static.block import Block
from game_object.static.energy_receptive_block import EnergyReceptiveBlock
from game_object.static.ladder import Ladder
from game_object.static.no_collision_block import NoCollisionBlock
from game_object.static.no_sides_block import NoSidesBlock
from graphics import graphics
from level.level import Level
from level.level_text import LevelText


# Key

# <space> = air
# B = a standard block/wall/whatever

def assign(level_text: LevelText):
    level = Level(level_text.dim)

    for i in range(0, level_text.dim[0]):
        for j in range(0, level_text.dim[1]):
            location = (i, j)
            chars = (level_text.background.get(location),
                     level_text.main.get(location),
                     level_text.foreground.get(location))

            if chars[1] == "B":
                surroundings = level_text.main.get_surrounding_pieces(location)
                edges = [[char != 'B' for char in row] for row in surroundings]

                level.set(location, Block(location, level.main_surface, graphics.get(
                    "platform_" + ("cross" if (location[0] + location[1]) % 2 else "box")).get_with_edge(edges)))

            elif chars[1] == "P":
                level.set_player_location(location)

            elif chars[1] == "L":
                above_location = (location[0], location[1] - 1)
                obj = Ladder(location, level.main_surface)
                if level_text.main.get(above_location) == " ":
                    obj.is_floor = True
                    obj.is_top_ladder = True
                    obj.image.blit(graphics.get("ladder_platform").get(), (0, 0))
                    obj.render()
                    level.set(above_location, NoCollisionBlock(above_location, level.main_surface, graphics.get("ladder_top").get()))
                level.set(location, obj)

            elif chars[1] == "C":
                level.set(location, NoCollisionBlock(location, level.main_surface, graphics.get("column").get()))

            elif chars[1] == "R":
                level.set(location, EnergyReceptiveBlock(location, level.main_surface, level.network_manager, graphics.get("receiver_inactive").get()))



    return level
