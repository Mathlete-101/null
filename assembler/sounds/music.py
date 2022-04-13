import os

from sound import sounds
from sound.music import Music


def assemble():
    sounds.add(Music(os.path.join("resources", "sounds", "midi", "dont_fall_behind_test.mid")), "test")

