from assembler.images import blocks, player
from assembler.levels import levels


def assemble():
    blocks.assemble()
    player.assemble()
    levels.assemble_levels()
