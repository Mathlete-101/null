import os

from assigner.assigner import assign
from level.level_text import LevelText, TextLayer


def check_level_exists(dir):
    return os.path.exists(os.path.join("resources", "levels", dir))

def load_level(dir):
    file_path = os.path.join('resources', 'levels', dir)
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
    level = assign(LevelText(grids["background"], grids["main"], grids["foreground"]), dir)
    level.initialize()
    return level
