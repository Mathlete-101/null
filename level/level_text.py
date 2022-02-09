from copy import deepcopy

import numpy

import assigner


# takes the raw file and turns it into a 2d array
# uses numpy to make sure that x is x and y is y
# stores it for consumption by a better class
class TextLayer:
    def __init__(self, text):
        if text:
            transformed_text = []
            for row in text:
                row = [x for x in row]
                if len(row) > 0 and row[len(row) - 1] == "\n":
                    row.pop()
                transformed_text.append(row)
            max_length = max([len(row) for row in transformed_text])
            self.dim = (max_length - 1, len(transformed_text))
            for row in transformed_text:
                row += [' ' for x in range(0, max_length - len(row))]

            grid = numpy.transpose(numpy.array(transformed_text))
            self.text = grid.tolist()
        else:
            self.text = None

    def get_level(self):
        return self.text

    def get(self, location):
        if self.text is None:
            return ' '
        try:
            return self.text[location[0]][location[1]]
        except IndexError:
            return 'B'

    def get_surrounded_level(self):
        if self.text is None:
            return None
        surrounded = deepcopy(self.text)
        surrounded = [['B' if surrounded[0][x] == 'B' else ' ' for x in range(0, len(surrounded[0]))]] + surrounded
        surrounded = surrounded + [['B' if surrounded[-1][x] == 'B' else ' ' for x in range(0, len(surrounded[-1]))]]
        full_surrounded = []
        for row in surrounded:
            full_surrounded += [['B'] + row + ['B']]
        return full_surrounded

    def get_surrounding_pieces(self, location):
        # location = (location[0], location[2])
        if location[0] >= self.dim[0] and location[1] >= self.dim[1]:
            raise IndexError("Error: location passed not within level text")
        if self.text is None:
            return [[False, False, False], [False, False, False], [False, False, False]]
        surrounded_a = self.get_surrounded_level()
        surrounded_b = surrounded_a[location[0]: location[0] + 3]
        surrounded = [row[location[1]: location[1] + 3] for row in surrounded_b]
        return surrounded


class LevelText:

    def __init__(self, background, main, foreground):
        self.background = TextLayer(background)
        self.main = TextLayer(main)
        self.foreground = TextLayer(foreground)
        self.dim = self.main.dim

    def assign(self):
        assigner.assigner.assign(self)
