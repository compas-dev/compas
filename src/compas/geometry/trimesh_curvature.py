from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import pluggable


@pluggable(category="trimesh")
def trimesh_gaussian_curvature(M):
    """Compute the discrete gaussian curvature of a triangle mesh.

    Parameters
    ----------
    M : tuple[sequence[[float, float, float] | :class:`compas.geometry.Point`], sequence[[int, int, int]]]
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    list[float]
        The discrete gaussian curvature per vertex.

    Examples
    --------
    >>>

    """
    pi2 = 2 * pi
    # key_xyz = {key: mesh.vertex_attributes(key, "xyz") for key in mesh.vertices()}
    curvature = [0] * mesh.number_of_vertices()
    # for key in mesh.vertices():
    #     angles = []
    #     o = key_xyz[key]
    #     for u in mesh.vertex_neighbors(key):
    #         fkey = mesh.halfedge[key][u]
    #         if fkey is not None:
    #             vertices = mesh.face_vertices(fkey)
    #             v = vertices[vertices.index(key) - 1]
    #             a = key_xyz[u]
    #             b = key_xyz[v]
    #             angles.append(angle_points(o, a, b))
    #     curvature.append(pi2 - sum(angles))
    for face in mesh.faces():
        vertices = mesh.face_vertices(face)
        for i in range(-1, len(vertices) - 1):
            u = vertices[i - 1]
            v = vertices[i]
            w = vertices[i + 1]
            a = mesh.vertex_coordinates(u)
            b = mesh.vertex_coordinates(v)
            c = mesh.vertex_coordinates(w)
            curvature.append(angle_points(a, b, c))
    return curvature


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
