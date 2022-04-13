from assembler.images import blocks, player
from assembler.sounds import sounds


def assemble():
    blocks.assemble()
    player.assemble()
    sounds.assemble()
