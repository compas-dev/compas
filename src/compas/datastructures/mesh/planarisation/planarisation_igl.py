from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = [
    'mesh_planarize_faces_igl',
]


def mesh_planarize_faces_igl(mesh, fixed=None, kmax=100, callback=None, callback_args=None):
    """Planarise a set of connected faces.

    Planarisation is implemented as a two-step iterative procedure. At every
    iteration, faces are first individually projected to their best-fit plane,
    and then the vertices are projected to the centroid of the disconnected
    corners of the faces.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.
    fixed : list, optional [None]
        A list of fixed vertices.
    kmax : int, optional [100]
        The number of iterations.
    d : float, optional [1.0]
        A damping factor.
    callback : callable, optional [None]
        A user-defined callback that is called after every iteration.
    callback_args : list, optional [None]
        A list of arguments to be passed to the callback function.

    Returns
    -------
    None

    """
    pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
