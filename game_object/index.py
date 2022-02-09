import math

from game_object.game_object import GameObject


class Bucket:
    def __init__(self):
        self.objects = []
        self.surrounding = []

    def set_surrounding_buckets(self, surrounding):
        self.surrounding = surrounding

    def add(self, obj):
        self.objects.append(obj)

    @property
    def nearby_objects(self):
        objs = []
        for bucket in self.surrounding:
            objs = objs.concat(bucket.objects)
        return objs

class Index:
    def __init__(self, dim):
        self.dim = dim
        self.grid = [[Bucket() for i in range(0, dim[1])] for i in range(0, dim[0])]
        for i in range(0, dim[0]):
            for j in range(0, dim[1]):
                # print(self.grid[i][j], [x[max(j-2,0):min(j+2,)] for x in self.grid[i-2:i+2])
                # self.grid[i][j].set_surrounding_buckets(self.grid)
                pass

    def add(self, object: GameObject):
        self.grid[math.floor(object.x)][math.floor(object.y)].add(object)
