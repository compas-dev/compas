from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import pi

from compas.geometry import angle_points


__all__ = [
    'trimesh_mean_curvature',
    'trimesh_gaussian_curvature'
]


def trimesh_mean_curvature(mesh):
    pass


def trimesh_gaussian_curvature(mesh):
    r"""Compute the gaussian curvature at the vertices of a triangle mesh using the angular deficit.

    Parameters
    ----------
    mesh : compas.oatastructures.Mesh
        The triangle mesh data structure.

    Returns
    -------
    list of float
        Per vertex curvature values.

    Warnings
    --------
    This function will not check if the provided mesh is actually a triangle mesh.
    It will just treat it as such...

    Notes
    -----
    The angular deficit at a vertex is defined as the difference between a full
    circle angle (:math:`2\pi`) and the sum of the angles in the adjacent trianlges.

    .. math::

        k_{G}(v_{i}) = 2\pi - \sum_{j \in N(i)} \teta_{ij}

    where :math:`N(i)` are the triangles incident on vertex :math:`i` and :math:`\teta_{ij}`
    is the angle at vertex :math:`i` in triangle :math:`j`.

    """
    pi2 = 2 * pi
    key_xyz = {key: mesh.vertex_attributes(key, 'xyz') for key in mesh.vertices()}
    curvature = []
    for key in mesh.vertices():
        angles = []
        o = key_xyz[key]
        for u in mesh.vertex_neighbors(key):
            fkey = mesh.halfedge[key][u]
            if fkey is not None:
                vertices = mesh.face_vertices(fkey)
                v = vertices[vertices.index(key) - 1]
                a = key_xyz[u]
                b = key_xyz[v]
                angles.append(angle_points(o, a, b))
        curvature.append(pi2 - sum(angles))
    return curvature


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod(globs=globals())
