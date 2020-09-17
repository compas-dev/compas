from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from numpy import asarray

from compas.geometry import transform_points_numpy

from compas.geometry.collections import CollectionNumpy


__all__ = ['PointCollectionNumpy']


class PointCollectionNumpy(CollectionNumpy):

    def __init__(self, points):
        self._data = []
        self._items = []
        self.points = points

    @property
    def points(self):
        for item, data in zip(self._items, self._data):
            item[:] = data[:]
        return self.items

    @points.setter
    def points(self, points):
        self._items = points
        self._data = asarray(points)

    def __getitem__(self, key):
        if isinstance(key, slice):
            items = []
            for i in range(*key.indices(len(self._items))):
                item = self._items[i]
                item[:] = self._data[i][:]
                items.append(item)
            return items
        self._items[key][:] = self._data[key][:]
        return self._items[key]

    def __setitem__(self, key, point):
        self._items[key] = point
        self._data[key] = point[:]

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def copy(self):
        return PointCollectionNumpy([point.copy() for point in self._items])

    def transform(self, X):
        transform_points_numpy(self._data, X)

    def transformed(self, X):
        collection = self.copy()
        collection.transform(X)
        return collection


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import timeit

    setup = """
from math import radians
from compas.geometry import Rotation
from compas.geometry import Point
from compas.geometry import PointCollectionNumpy
from compas.geometry import Vector
from compas.geometry import pointcloud
R = Rotation.from_axis_and_angle(Vector.Zaxis(), radians(30))
collection = PointCollectionNumpy([Point(*xyz) for xyz in pointcloud(10000, (0, 10), (0, 3), (0, 2))])
"""

    code = """
collection.transform(R)
"""

    number = 100

    result = min(timeit.repeat(code, setup=setup, repeat=10, number=number))
    print(result)
    print(result / number)
