from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Point
from .collection import Collection


class PointCollection(Collection):

    def __init__(self, points):
        self._items = points

    # ==========================================================================
    # items
    # ==========================================================================

    @property
    def itype(self):
        return Point

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, items):
        self._items = []
        if items:
            for item in items:
                if not isinstance(item, Point):
                    item = Point(*item)
                self._items.append(item)

    # ==========================================================================
    # data
    # ==========================================================================

    # ==========================================================================
    # properties
    # ==========================================================================

    # ==========================================================================
    # customization
    # ==========================================================================

    # ==========================================================================
    # constructors
    # ==========================================================================

    # ==========================================================================
    # methods
    # ==========================================================================
