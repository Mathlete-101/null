graphics = {}


def add(graphic, name):
    graphics[name] = graphic


def get(name):
    return graphics[name]

def add_reflection_rotation(g, name):
    fg = g.get_reflection()
    add(g, name + "0")
    add(g.get_rotation(90), name + "1")
    add(g.get_rotation(180), name + "2")
    add(g.get_rotation(270), name + "3")
    add(fg, name + "4")
    add(fg.get_rotation(90), name + "5")
    add(fg.get_rotation(180), name + "6")
    add(fg.get_rotation(270), name + "7")