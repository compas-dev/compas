from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas import IPY

from .halfedge import HalfEdge  # noqa: F401
from .mesh import BaseMesh  # noqa: F401
from .operations import *  # noqa: F401 F403
from .clean import *  # noqa: F401 F403

if not IPY:
    from .matrices import *  # noqa: F401 F403

__all__ = [name for name in dir() if not name.startswith('_')]
