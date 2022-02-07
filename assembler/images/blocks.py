from assembler.images import energy_parts, platforms, ladder, columns, doors


def assemble():
    energy_parts.assemble()
    platforms.assemble()
    ladder.assemble()
    columns.assemble()
    doors.assemble()
