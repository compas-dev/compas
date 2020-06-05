from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from numpy import array
from compas.numerical import grad


__all__ = ['trimesh_descent']


def trimesh_descent(trimesh):
    """"""
    vertices, faces = trimesh.to_vertices_and_faces()
    V = array(vertices)
    F = array(faces)
    G = grad(V, F)
    sfield = V[:, 2].reshape((-1, 1))
    vfield = - G.dot(sfield)
    return vfield.reshape((-1, 3), order='F').tolist()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod(globs=globals())
