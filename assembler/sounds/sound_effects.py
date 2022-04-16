# Sound files were generated from the following website: sfxr.me
# Future self, if you want different sounds, just go there and make them
import os

import pygame

from sound import sounds


def assemble():
    # Load all sounds from the folder resources/sounds/sfx
    for name in os.listdir(os.path.join("resources", "sounds", "sfx")):
        dir = os.path.join("resources", "sounds", "sfx", name)
        sound_name = name.split(".")[0]
        sounds.add_sound(pygame.mixer.Sound(dir), sound_name)