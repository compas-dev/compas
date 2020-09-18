from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import pluggable


__all__ = ['quadmesh_planarize']


@pluggable(category='quadmesh')
def quadmesh_planarize(M, kmax=500, maxdev=0.005):
    """Planarize the faces of a quad mesh.

    Parameters
    ----------
    M : (list, list)
        A quad mesh represented by a list of vertices and a list of faces.
    kmax : int, optional
        The maximum number of iterations.
        Default is ``500``.
    maxdev : float, optional
        The maximum deviation from planar.
        Default is ``0.005``.

    Returns
    -------
    list
        The coordinates of the new vertices.

    Examples
    --------
    >>>

    """
    raise NotImplementedError
