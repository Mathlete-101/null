import graphics.graphics
from engine.settings import settings
from game_object.static import collectible
from game_object.static.air import Air
from game_object.static.block import Block
from game_object.static.collectible import Collectible
from game_object.static.door_block import DoorBlock
from game_object.static.energy.energy_delay_block import EnergyDelayBlock
from game_object.static.energy.energy_force_field_block import EnergyForceFieldBlock
from game_object.static.energy.energy_recharge_block import EnergyRechargeBlock
from game_object.static.energy.energy_timed_receptive_block import EnergyTimedReceptiveBlock
from game_object.static.energy.energy_toggle_receptive_block import EnergyToggleReceptiveBlock
from game_object.static.energy.energy_transistor_block import EnergyTransistorBlock
from game_object.static.energy.energy_wire_block import EnergyWireBlock
from game_object.static.energy.energy_wire_no_collision_block import EnergyWireNoCollisionBlock
from game_object.static.ladder import Ladder
from game_object.static.laser_through_block import LaserThroughBlock
from game_object.static.no_collision_block import NoCollisionBlock
from graphics import graphics
from level.level import Level
from level.level_text import LevelText


# Key

# <space> = air
# B = a standard block/wall/whatever
from misc.sign import GameSign
from tools import duple, text

common_air = Air((0, 0))

def apply_background(character, loc, level):
    # Background Stuff
    if character in ["W", "w"]:
        level.world_surface.blit(
            graphics.get("inner_wall" + ("_dark" if character == "w" else "")).get_reflected(x=False, y=loc[0] % 2),
            duple.scale(loc, 42))
    elif character in ["E", "e"]:
        level.world_surface.blit(
            graphics.get("inner_wall" + ("_dark" if character == "e" else "") + "_right").get_reflected(x=False,
                                                                                                        y=loc[0] % 2),
            duple.scale(loc, 42))
    elif character in ["Q", "q"]:
        level.world_surface.blit(
            graphics.get("inner_wall" + ("_dark" if character == "q" else "") + "_left").get_reflected(x=False,
                                                                                                       y=loc[0] % 2),
            duple.add(duple.scale(loc, 42), (12, 0)))
    elif character in ["A"]:
        level.world_surface.blit(graphics.get("inner_wall_alt_a").get(), duple.scale(loc, 42))


def assign_individual(location, level, level_text, meta_data, level_name):
    chars = (level_text.background.get(location),
             level_text.main.get(location),
             level_text.foreground.get(location))
    # Main Pieces
    if chars[1] == "B":
        surroundings = level_text.main.get_surrounding_pieces(location)
        edges = [[char != 'B' for char in row] for row in surroundings]

        level.set(location, Block(location, level.world_surface, graphics.get(
            "platform_" + ("cross" if (location[0] + location[1]) % 2 else "box") + (
                "_alt" if location[1] < meta_data["floor_level"] else "")).get_with_edge(edges)))
        if location[1] < meta_data["floor_level"]:
            apply_background('w', location, level)
    elif chars[1] == "b":
        level.set(location, Block(location, level.world_surface, graphics.get("platform_thin").get()))

    elif chars[1] == "c":
        surroundings = level_text.main.get_surrounding_pieces(location)
        background_surroundings = level_text.background.get_surrounding_pieces(location)
        edges = [[surroundings[r][c] != 'c' or background_surroundings[r][c] != chars[0] for c in range(3)] for r in
                 range(3)]
        level.set(location, Block(location, level.world_surface, graphics.get("large_crate").get_with_edge(edges)))

    elif chars[1] == " ":
        level.set(location, common_air)

    elif chars[1] == "P":
        level.set(location,
                  DoorBlock(location, level.world_surface, graphics.get("door_" + level_name).get(), level, -1))

        level.player_setup(location)

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
        graphic_name = "column"

        background_letter = chars[0]

        if level_text.main.get(duple.add(location, (0, 1))) != 'C':
            if not chars[0].isdigit() or int(chars[0]) == 0:
                graphic_name += "_base"
            # insert special backgrounds for columns that aren't bases but need a background
            else:
                if chars[0].isdigit():
                    background_number = int(chars[0])
                    if background_number == 2:
                        apply_background('W', location, level)
                        background_letter = 'W'
                    elif background_number == 3:
                        apply_background('Q', location, level)
                        background_letter = 'Q'
                    elif background_number == 4:
                        apply_background('q', location, level)
                        background_letter = 'q'

        # pick the columm graphic based on the background
        if background_letter == ' ':
            graphic_name += "_blue"
        elif text.is_upper_case(background_letter):
            graphic_name += "_light"
        else:
            graphic_name += "_dark"

        level.set(location, NoCollisionBlock(location, level.world_surface, graphics.get(graphic_name).get()))

    elif chars[1] == "R":
        level.set(location, EnergyTimedReceptiveBlock(location, level.render_surface, level.network_manager,
                                                      graphics.get("energy_receiver_time")))

    elif chars[1] == "W":
        level.set(location, EnergyWireBlock(location, level.render_surface, level.network_manager,
                                            graphics.get("energy_wire_through")))

    elif chars[1] == "T":
        level.set(location, EnergyToggleReceptiveBlock(location, level.render_surface, level.network_manager,
                                                       graphics.get("energy_receiver_toggle")))
        if chars[0] == "1":
            level.main[location[0]][location[1]].supplying = True

    elif chars[1] == "D":
        graphic = graphics.get("energy_delay")
        rotation = int(chars[0] if str.isnumeric(chars[0]) else 0)
        graphics_rotation = rotation
        if graphics_rotation % 2 == 0:
            graphics_rotation += 2
            graphics_rotation %= 4
        graphic = graphic.get_rotation(graphics_rotation)
        level.set(location, EnergyDelayBlock(location, level.render_surface, level.network_manager, graphic, rotation))

    elif chars[1] == "t":
        if not str.isnumeric(chars[0]):
            orientation = 0
        else:
            orientation = int(chars[0])
        reflection = bool(orientation % 2)
        rotation = orientation // 2
        graphic = graphics.get("energy_transistor")
        graphic = graphic.get_reflection(reflection)
        graphic = graphic.get_rotation(abs(4 - rotation))
        level.set(location,
                  EnergyTransistorBlock(location, level.render_surface, level.network_manager, graphic, reflection,
                                        rotation))

    elif chars[1] == "F":
        level.set(location, EnergyForceFieldBlock(location, level.render_surface, level.network_manager,
                                                  graphics.get("energy_force_field")))

    elif chars[1] == "E":
        level.set(location,
                  EnergyRechargeBlock(location, level.render_surface, level.world_surface, level.network_manager,
                                      graphics.get("energy_recharge")))

    elif chars[1] == "d":
        level.set(location,
                  DoorBlock(location, level.world_surface, graphics.get("door_exit").get(), level, int(level_name)))

    elif chars[1] in ["1", "2", "3"]:
        block = Collectible(location, level.world_surface, level.render_surface,
                            graphics.get("data_stick_" + chars[1]).get(),
                            collectible.get_data_stick_effect(25 * pow(5, int(chars[1]))), ["data_stick"])
        level.set(location, block)
        level.continuous_block_sprite_group.add(block)
    elif chars[1] == "Q":
        level.set(location, EnergyWireNoCollisionBlock(location, level.render_surface, level.network_manager,
                                                       graphics.get("energy_wire_through_dark")))
    elif chars[1] == "p":
        level.set(location,
                  LaserThroughBlock(location, level.render_surface, graphics.get("platform_laser_through").get()))
    elif chars[1] == "X":
        block = Collectible(location, level.world_surface, level.render_surface, graphics.get("movement_belt").get(),
                            collectible.get_movement_belt_effect(), ["movement_belt"])
        level.set(location, block)
        level.continuous_block_sprite_group.add(block)

    # add the block to the block sprite group and its proper column sprite group
    if len({"air", "collectible"}.intersection(level.main[location[0]][location[1]].tags)) == 0:
        level.block_sprite_group.add(level.main[location[0]][location[1]])
    level.col_groups[location[0]].add(level.main[location[0]][location[1]])

    # Direct backgrounds
    apply_background(chars[0], location, level)


def assign(level_text: LevelText, level_name, meta_data: dict, level_type):
    # basically a factory function for the Level object
    if "player_count" not in meta_data:
        meta_data["player_count"] = 1

    level = Level(level_text.dim, meta_data["player_count"], level_type, level_text, meta_data, level_name)
    level.level_number = int(level_name)

    if "movement_belt" in meta_data:
        for player in level.players:
            player.movement_belt = meta_data["movement_belt"]

    if "floor_level" not in meta_data:
        meta_data["floor_level"] = 0

    # Create signs
    if "signs" in meta_data:
        if settings.get("assistive_signs"):
            for sign in meta_data["signs"]:
                position = (sign["position"]["x"] - 1, sign["position"]["y"] - 1)
                level.world_surface.blit(GameSign(sign["lines"]).surface, duple.scale(position, 42))
        else:
            for sign in meta_data["signs"]:
                position = (sign["position"]["x"] - 1, sign["position"]["y"] - 1)
                sign_obj = GameSign(sign["lines"])
                for location in [duple.add(position, (x, 0)) for x in range(sign_obj.width)]:
                    level_text.main.text[location[0]][location[1]] = "B"

    for i in range(0, level_text.dim[0]):
        for j in range(0, level_text.dim[1]):
            location = (i, j)
            assign_individual(location, level, level_text, meta_data, level_name)

    return level
