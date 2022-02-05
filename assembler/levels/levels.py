import os

from assigner.assigner import assign
from level.level_text import LevelText, TextLayer

levels = {}


def assemble_levels():
    levels_dir = os.path.join('resources', 'levels')
    for directory in os.listdir(levels_dir):
        file_path = os.path.join(levels_dir, directory)
        grids = {}
        for sub_path in ["foreground", "background", "main"]:
            final_path = os.path.join(file_path, sub_path) + ".txt"
            if os.path.exists(final_path):
                with open(final_path, 'r') as file:
                    lines = file.readlines()
                    grid = []
                    for line in lines:
                        grid.append([x for x in line])
                    grids[sub_path] = grid
            else:
                grids[sub_path] = [[]]
        levels[directory] = assign(LevelText(grids["background"], grids["main"], grids["foreground"]))
        levels[directory].network_manager.initialize()


def get_level(level):
    return level
