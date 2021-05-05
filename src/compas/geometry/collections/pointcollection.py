from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry.collections import Collection

__all__ = ['PointCollection']


class PointCollection(Collection):

    def __init__(self, points):
        self._items = points

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [self._items[i] for i in range(*key.indices(len(self._items)))]
        return self._items[key]

    def __setitem__(self, key, value):
        self._items[key] = value

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def copy(self):
        return PointCollection([point.copy() for point in self._items])

    def transform(self, X):
        for item in self._items:
            item.transform(X)

    def transformed(self, X):
        collection = self.copy()
        collection.transform(X)
        return collection
