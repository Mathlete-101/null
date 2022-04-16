import os

from sound import sounds
from sound.music import Music


def assemble():
    """Load all sounds from the directory resources/sounds/music/. The name of the song is the part of the file name before the ."""
    music_dir = os.path.join("resources", "sounds", "music")
    for filename in os.listdir(music_dir):
        music = Music(os.path.join(music_dir, filename), filename.split(".")[1])
        sounds.add_music(music, filename.split(".")[0])
