from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

from .collection import Collection  # noqa: F401

if not compas.IPY:
    from .collection_numpy import CollectionNumpy  # noqa: F401

from .pointcollection import PointCollection  # noqa: F401

if not compas.IPY:
    from .pointcollection_numpy import PointCollectionNumpy  # noqa: F401


__all__ = [name for name in dir() if not name.startswith('__')]
