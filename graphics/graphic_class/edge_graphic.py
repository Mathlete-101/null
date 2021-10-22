import pygame.transform

from graphics.graphic_class.graphic import Graphic
import numpy


class EdgeGraphic(Graphic):

    def __init__(self, img, edge, outer_corner, inner_corner):
        super().__init__(img)
        self.edge = edge
        self.inner_corner = inner_corner
        self.outer_corner = outer_corner

    def get_with_edge(self, surroundings):

        surroundings_array = numpy.array(surroundings)
        result_img = self.get().copy()

        for i in range(0, 4):
            if surroundings_array[1][0]:
                result_img.blit(self.edge, (0, 0))

            result_img = pygame.transform.rotate(result_img, 270)
            surroundings_array = numpy.rot90(surroundings_array)

        for i in range(0, 4):
            if surroundings_array[0][0] and surroundings_array[0][1] == surroundings_array[1][0]:
                if surroundings_array[0][1]:
                    result_img.blit(self.inner_corner, (0, 0))
                else:
                    result_img.blit(self.outer_corner, (0, 0))

            result_img = pygame.transform.rotate(result_img, 270)
            surroundings_array = numpy.rot90(surroundings_array)

        return result_img

