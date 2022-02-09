import tools.transform
from misc.wrapped_sprite import WrappedSprite
from tools.text import render_font_cool as Text, get_monospaced_sprites
from tools import duple
from tools.transform import scale_factor


class Leader:
    def __init__(self, name, score, placeholder=False):
        self.name = name
        self.score = score
        self.placeholder = placeholder
        self.spacing = 40
        self.name_sprites = []

    def position(self, position, label):
        self.name_sprites = list(get_monospaced_sprites(self.name, position, self.spacing).sprites())
        return self.name_sprites + \
               list(get_monospaced_sprites(format(self.score, "06"), duple.add(position, (self.spacing * 4, 0)), self.spacing)) + \
               [WrappedSprite(tools.transform.scale_factor(Text(label), 3), duple.subtract(position, (self.spacing * 3, 0)))]

