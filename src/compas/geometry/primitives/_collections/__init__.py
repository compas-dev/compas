from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

from .collection import Collection
from .pointcollection import PointCollection

if not compas.IPY:
    from .collection_numpy import CollectionNumpy
    from .pointcollection_numpy import PointCollectionNumpy


__all__ = [name for name in dir() if not name.startswith('__')]
