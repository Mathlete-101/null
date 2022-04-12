import os

from assigner.assigner import assign
from level.level_text import LevelText, TextLayer
import json


def get_level_dir(level_type, level_dir):
    return os.path.join("resources", "levels", level_type, level_dir)


def check_level_exists(level_type, level_dir):
    return os.path.exists(get_level_dir(level_type, level_dir))


def get_json_file(level_type, level_dir):
    """Returns an object from the json file with the given directory. Json files are named meta.json."""
    with open(os.path.join(get_level_dir(level_type, level_dir), "meta.json")) as f:
        return json.load(f)


def load_level(level_type, level_dir):
    file_path = get_level_dir(level_type, level_dir)
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
    level = assign(LevelText(grids["background"], grids["main"], grids["foreground"]), level_dir, get_json_file(level_type, level_dir))
    level.initialize()
    return level
