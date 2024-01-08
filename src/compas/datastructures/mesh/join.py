from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.tolerance import TOL
from compas.utilities import pairwise


def mesh_weld(mesh, precision=None, cls=None):
    """Weld vertices of a mesh within some precision distance.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A mesh.
    precision : int, optional
        Precision for converting numbers to strings.
        Default is :attr:`TOL.precision`.
    cls : Type[:class:`compas.datastructures.Mesh`], optional
        Type of the welded mesh.
        This defaults to the type of the first mesh in the list.

    Returns
    -------
    :class:`compas.datastructures.Mesh`
        The welded mesh.

    """
    if cls is None:
        cls = type(mesh)

    geo = TOL.geometric_key

    vertex_xyz = {vertex: mesh.vertex_coordinates(vertex) for vertex in mesh.vertices()}
    gkey_vertex = {geo(xyz, precision): vertex for vertex, xyz in vertex_xyz.items()}
    gkey_index = {gkey: index for index, gkey in enumerate(gkey_vertex)}

    vertices = [vertex_xyz[vertex] for gkey, vertex in gkey_vertex.items()]
    faces = []
    for face in mesh.faces():
        indices = []
        for vertex in mesh.face_vertices(face):
            gkey = geo(vertex_xyz[vertex], precision)
            indices.append(gkey_index[gkey])
        faces.append(indices)

    faces[:] = [[u for u, v in pairwise(indices + indices[:1]) if u != v] for indices in faces]
    faces[:] = [indices for indices in faces if len(indices) > 2]

    mesh = cls.from_vertices_and_faces(vertices, faces)
    return mesh


def meshes_join(meshes, cls=None):
    """Join meshes without welding.

    Parameters
    ----------
    meshes : list[:class:`compas.datastructures.Mesh`]
        A list of meshes.
    cls : Type[:class:`compas.datastructures.Mesh`], optional
        The type of the joined mesh.
        This defaults to the type of the first mesh in the list.

    Returns
    -------
    :class:`compas.datastructures.Mesh`
        The joined mesh.

    Examples
    --------
    >>> from compas.datastructures import Mesh
    >>> from compas.datastructures import meshes_join
    >>> vertices_1 = [[0, 0, 0], [0, 500, 0], [500, 500, 0], [500, 0, 0]]
    >>> vertices_2 = [[500, 0, 0], [500, 500, 0], [1000, 500, 0], [1000, 0, 0]]
    >>> faces = [[0, 1, 2, 3]]
    >>> mesh_1 = Mesh.from_vertices_and_faces(vertices_1, faces)
    >>> mesh_2 = Mesh.from_vertices_and_faces(vertices_2, faces)
    >>> mesh = meshes_join([mesh_1, mesh_2])
    >>> mesh.number_of_vertices()
    8
    >>> mesh.number_of_faces()
    2

    """
    if cls is None:
        cls = type(meshes[0])

    vertices = []
    faces = []

    for mesh in meshes:
        offset = len(vertices)
        vertex_index = {vertex: offset + i for i, vertex in enumerate(mesh.vertices())}
        vertices += [mesh.vertex_coordinates(vertex) for vertex in mesh.vertices()]
        faces += [[vertex_index[vertex] for vertex in mesh.face_vertices(face)] for face in mesh.faces()]

    return cls.from_vertices_and_faces(vertices, faces)


def meshes_join_and_weld(meshes, precision=None, cls=None):
    """Join and and weld meshes within some precision distance.

    Parameters
    ----------
    meshes : list[:class:`compas.datastructures.Mesh`]
        A list of meshes.
    precision : int, optional
        Precision for converting numbers to strings.
        Default is :attr:`TOL.precision`.
    cls : Type[:class:`compas.datastructures.Mesh`], optional
        The type of return mesh.

    Returns
    -------
    :class:`compas.datastructures.Mesh`
        The joined and welded mesh.

    """
    return mesh_weld(meshes_join(meshes, cls=cls), precision=precision)
