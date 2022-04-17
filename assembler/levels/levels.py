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
    longest_line = 0
    for sub_path in ["foreground", "background", "main"]:
        final_path = os.path.join(file_path, sub_path) + ".txt"
        if os.path.exists(final_path):
            with open(final_path, 'r') as file:
                lines = file.readlines()
                grid = []
                for line in lines:
                    grid.append([x for x in line])
                    longest_line = max(longest_line, len(line))
                grids[sub_path] = grid
        else:
            grids[sub_path] = [[]]
    # normalize line length
    for grid in grids.values():
        for line in grid:
            line += [" "] * (longest_line - len(line))
    level = assign(LevelText(grids["background"], grids["main"], grids["foreground"]), level_dir, get_json_file(level_type, level_dir), level_type)
    level.initialize()
    return level


def save_level(level_text: LevelText, level_type, level_dir):
    file_path = get_level_dir(level_type, level_dir)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    for sub_path in ["foreground", "background", "main"]:
        if level_text[sub_path].text is None:
            continue
        final_path = os.path.join(file_path, sub_path) + ".txt"
        with open(final_path, 'w') as file:
            for line in level_text.get_raw(sub_path):
                file.write("".join(filter(lambda c: c != '\n', line)) + "\n")