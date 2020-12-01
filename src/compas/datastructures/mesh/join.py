from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import pairwise
from compas.utilities import geometric_key

__all__ = [
    'mesh_weld',
    'meshes_join',
    'meshes_join_and_weld'
]


def mesh_weld(mesh, precision=None, cls=None):
    """Weld vertices of a mesh within some precision distance.

    Parameters
    ----------
    mesh : Mesh
        A mesh.
    precision: str (None)
        Tolerance distance for welding.
    cls : type (None)
        Type of the welded mesh.
        This defaults to the type of the first mesh in the list.

    Returns
    -------
    mesh
        The welded mesh.

    """
    if cls is None:
        cls = type(mesh)

    geo = geometric_key

    key_xyz = {key: mesh.vertex_coordinates(key) for key in mesh.vertices()}
    gkey_key = {geo(xyz, precision): key for key, xyz in key_xyz.items()}
    gkey_index = {gkey: index for index, gkey in enumerate(gkey_key)}

    vertices = [key_xyz[key] for gkey, key in gkey_key.items()]
    faces = [[gkey_index[geo(key_xyz[key], precision)] for key in mesh.face_vertices(fkey)] for fkey in mesh.faces()]

    faces[:] = [[u for u, v in pairwise(face + face[:1]) if u != v] for face in faces]
    faces[:] = [face for face in faces if len(face) > 2]  # make sure no face has less than 3 vertices

    mesh = cls.from_vertices_and_faces(vertices, faces)
    return mesh


def meshes_join(meshes, cls=None):
    """Join meshes without welding.

    Parameters
    ----------
    meshes : list
        A list of meshes.
    cls : type (None)
        The type of the joined mesh.
        This defaults to the type of the first mesh in the list.

    Returns
    -------
    mesh
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
        key_index = ({key: len(vertices) + i for i, key in enumerate(mesh.vertices())})
        vertices += [mesh.vertex_coordinates(key) for key in mesh.vertices()]
        faces += [[key_index[key] for key in mesh.face_vertices(fkey)] for fkey in mesh.faces()]

    return cls.from_vertices_and_faces(vertices, faces)


def meshes_join_and_weld(meshes, precision=None, cls=None):
    """Join and and weld meshes within some precision distance.

    Parameters
    ----------
    meshes : list
        A list of meshes.
    precision: str
        Tolerance distance for welding.

    Returns
    -------
    mesh
        The joined and welded mesh.

    """
    return mesh_weld(meshes_join(meshes, cls=cls), precision=precision)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    # from compas.datastructures import Mesh
    # from compas_plotters import MeshPlotter

    # vertices = [[0, 0, 0], [0.04, 0, 0], [1.0, 0, 0], [1.0, 1.0, 0], [0, 1.0, 0]]
    # faces = [[0, 1, 2, 3, 4]]

    # mesh = Mesh.from_vertices_and_faces(vertices, faces)
    # mesh = mesh_weld(mesh, precision='1f')

    # plotter = MeshPlotter(mesh, figsize=(10, 7))
    # plotter.draw_vertices(text={key: "{:.3f}".format(mesh.vertex[key]['x']) for key in mesh.vertices()}, radius=0.03)
    # plotter.draw_edges()
    # plotter.show()

    import doctest
    doctest.testmod(globs=globals())
