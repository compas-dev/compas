from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.datastructures.volmesh.core import BaseVolMesh

from compas.datastructures.volmesh.bbox import volmesh_bounding_box


__all__ = ['VolMesh']


class VolMesh(BaseVolMesh):
    """Implementation of the base volmesh data structure that adds some of the mesh algorithms as methods.

    """

    bounding_box = volmesh_bounding_box


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod(globs=globals())
