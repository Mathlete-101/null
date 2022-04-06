import os.path

import pygame.font
import tools
from misc.wrapped_sprite import WrappedSprite
from tools import duple

minecraft_font: pygame.font.Font = None


def render_font_cool(text, color1=(254, 255, 255), color2=(0, 0, 0), zoom=1):
    top = minecraft_font.render(text, False, color1)
    bottom = minecraft_font.render(text, False, color2)
    combined = tools.transform.get_clear_surface(tools.duple.add(top.get_size(), (2, 2)))
    combined.blit(bottom, (2, 2))
    combined.blit(top, (0, 0))
    return tools.transform.scale_factor(combined, zoom)


def get_monospaced_sprites(text, position, space, zoom=1):
    return pygame.sprite.Group([WrappedSprite(tools.transform.scale_factor(render_font_cool(text[x]), 3), duple.add(position, (x * space, 0))) for x in range(len(text))])


def get_monospaced_sprites_size(text, space, zoom=1):
    return space * (len(text) - 1) + 3 * (minecraft_font.metrics(text[-1])[0][1] + 2) * zoom, minecraft_font.metrics(text[0])[0][3]


def is_upper_case(text):
    return text == text.upper()