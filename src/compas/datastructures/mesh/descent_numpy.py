from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from numpy import array
from compas.geometry import trimesh_gradient_numpy


def trimesh_descent(trimesh):
    """Compute the gradient per face of the heightfield of the vertices of the mesh.

    Parameters
    ----------
    trimesh : :class:`compas.datastructures.Mesh`
        The triangle mesh.

    Returns
    -------
    list[list[float]]
        A list of vectors with one vector per face.

    """
    vertices, faces = trimesh.to_vertices_and_faces()
    V = array(vertices)
    F = array(faces)
    G = trimesh_gradient_numpy((V, F))
    sfield = V[:, 2].reshape((-1, 1))
    vfield = -G.dot(sfield)
    return vfield.reshape((-1, 3), order="F").tolist()
