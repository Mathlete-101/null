from assembler.sounds import sound_effects, music


# This function is called when the sound manager is loaded because it depends on the pygame mixer library
def assemble():
    music.assemble()
    sound_effects.assemble()
