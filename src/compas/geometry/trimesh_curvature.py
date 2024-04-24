from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import pi

from compas.geometry import angle_points
from compas.itertools import window
from compas.plugins import pluggable


@pluggable(category="trimesh")
def trimesh_gaussian_curvature(M):
    r"""Compute the discrete gaussian curvature of a triangle mesh.

    Parameters
    ----------
    M : tuple[sequence[[float, float, float] | :class:`compas.geometry.Point`], sequence[[int, int, int]]]
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    list[float]
        The discrete gaussian curvature per vertex.

    Warnings
    --------
    The default implementation willnot check if the mesh is a triangle mesh.
    It will simpliy compute the curvature at every vertex as if it were surrounded by triangles.
    This requires the faces of the mesh to be at least convex polygons.

    Notes
    -----
    The angular deficit at a vertex is defined as the difference between a full
    circle angle (:math:`2\pi`) and the sum of the angles in the adjacent trianlges.

    .. math::

        k_{G}(v_{i}) = 2\pi - \sum_{j \in N(i)} \theta_{ij}

    where :math:`N(i)` are the triangles incident on vertex :math:`i` and :math:`\theta_{ij}`
    is the angle at vertex :math:`i` in triangle :math:`j`.

    Examples
    --------
    >>>

    """
    vertices, faces = M
    pi2 = 2 * pi
    curvature = [0] * len(vertices)
    for face in faces:
        for u, v, w in window(face + face[0:2], 3):
            a = vertices[u]
            b = vertices[v]
            c = vertices[w]
            curvature[u] += angle_points(a, b, c)
            curvature[v] += angle_points(b, a, c)
            curvature[w] += angle_points(c, a, b)
    return [pi2 - c for c in curvature]


trimesh_gaussian_curvature.__pluggable__ = True


@pluggable(category="trimesh")
def trimesh_principal_curvature(M):
    """Compute the principal curvature directions of a triangle mesh.

    Parameters
    ----------
    M : tuple[sequence[[float, float, float] | :class:`compas.geometry.Point`], sequence[[int, int, int]]]
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    list[tuple[[float, float, float], [float, float]]]
        The curvature directions per vertex.

    Examples
    --------
    >>>

    """
    raise NotImplementedError


trimesh_principal_curvature.__pluggable__ = True


@pluggable(category="trimesh")
def trimesh_mean_curvature(M):
    """Compute the discrete mean curvature of a triangle mesh.

    Parameters
    ----------
    M : tuple[sequence[[float, float, float] | :class:`compas.geometry.Point`], sequence[[int, int, int]]]
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    list[float]
        The discrete mean curvature per vertex.

    Examples
    --------
    >>>

    """
    raise NotImplementedError


trimesh_mean_curvature.__pluggable__ = True
