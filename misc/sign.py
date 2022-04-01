import pygame

import tools.text
from tools import duple
from graphics import graphics


class GameSign:
    def __init__(self, text_lines):
        self.offset = (10, 10)
        self.text_lines = text_lines
        self.rendered_text_lines = [tools.text.render_font_cool(line) for line in text_lines]
        self.longest_line = max(self.rendered_text_lines, key=lambda x: x.get_width())
        self.text_width = self.longest_line.get_width() + self.offset[0]
        self.width = self.text_width // 42 + 1
        self.height = len(text_lines)
        self.dim = (self.width, self.height)
        self.surface = pygame.Surface(duple.scale(self.dim, 42))
        print("locations")
        print("self.width:", self.width)
        print("self.height:", self.height)
        for i in range(self.width):
            for j in range(self.height):
                print(i, j)
                surroundings = [
                    [i == 0 and j == 0, i == 0, i == 0 and j == self.height - 1],
                    [j == 0, False, j == self.height - 1],
                    [i == self.width - 1 and j == 0, i == self.width - 1, i == self.width - 1 and j == self.height - 1]
                ]
                print("surroundings:", surroundings)
                block = graphics.get("sign").get_with_edge(surroundings)
                location = duple.scale((i, j), 42)
                self.surface.blit(block, location)

        for i in range(self.height):
            self.surface.blit(self.rendered_text_lines[i], duple.add(self.offset, (0, i * 42)))

