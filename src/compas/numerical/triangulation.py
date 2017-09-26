from numpy import asarray
from scipy.spatial import Delaunay

from compas.datastructures.mesh import Mesh


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'delaunay_from_mesh',
    'delaunay_from_points',
    'delaunay_from_boundary',
]


def delaunay_from_mesh(mesh):
    """Return a Delaunay triangulation from a given mesh.

    Parameters:
        mesh (compas.datastructures.mesh.Mesh) :
            The original mesh.

    Returns:
        mesh :
            ...

    >>> ...

    """
    d = Delaunay(mesh.xy)
    return Mesh.from_vertices_and_faces(mesh.xyz, d.simplices)


def delaunay_from_points(points):
    """"""
    xyz = asarray(points)
    assert 2 <= xyz.shape[1], "At least xy xoordinates required."
    d = Delaunay(xyz[:, 0:2])
    return Mesh.from_vertices_and_faces(points, d.simplices)


# @see: _scripts
def delaunay_from_boundary(boundary):
    """"""
    raise NotImplementedError


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
