from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import geometric_key
from compas.utilities import reverse_geometric_key

__all__ = [
    'mesh_weld',
    'meshes_join',
    'meshes_join_and_weld'
]

def meshes_join(meshes, cls=None):
    """Join meshes without welding.
    Parameters
    ----------
    meshes : list
        A list of meshes.
    Returns
    -------
    mesh
        The joined mesh.
    """

    if cls is None:
        cls = type(meshes[0])

    vertices = []
    faces = []

    for mesh in meshes:
        # create vertex map based on geometric keys in dictionary with duplicates
        vertex_map = ({vkey: len(vertices) + i for i, vkey in enumerate(mesh.vertices())})
        # list vertices with coordinates
        vertices += [mesh.vertex_coordinates(vkey) for vkey in mesh.vertices()]
        # modify vertex indices in the faces
        faces += [ [vertex_map[vkey] for vkey in mesh.face_vertices(fkey)] for fkey in mesh.faces()]

    return cls.from_vertices_and_faces(vertices, faces)

def mesh_weld(mesh, precision=None, cls=None):
    """Weld vertices of a mesh within some precision distance.
    Parameters
    ----------
    mesh : Mesh
        A mesh.
    precision: str
        Tolerance distance for welding.
    Returns
    -------
    mesh
        The welded mesh.
    """

    if cls is None:
        cls = type(mesh)

    # create vertex map based on geometric keys in dictionary without duplicates
    vertex_map = {geometric_key(mesh.vertex_coordinates(vkey), precision): vkey for vkey in mesh.vertices()}
    # list vertices with coordinates
    vertices = [reverse_geometric_key(geom_key) for geom_key in vertex_map.keys()]
    # reorder vertex keys in vertex map
    vertex_map = {geom_key: i for i, geom_key in enumerate(vertex_map.keys())}
    # modify vertex indices in the faces
    faces = [ [vertex_map[geometric_key(mesh.vertex_coordinates(vkey), precision)] for vkey in mesh.face_vertices(fkey)] for fkey in mesh.faces()]

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

    if cls is None:
        cls = type(meshes[0])

    # create vertex map based on geometric keys in dictionary without duplicates
    vertex_map = {geometric_key(mesh.vertex_coordinates(vkey), precision): vkey for mesh in meshes for vkey in mesh.vertices()}
    # list vertices with coordinates
    vertices = [reverse_geometric_key(geom_key) for geom_key in vertex_map.keys()]
    # reorder vertex keys in vertex map
    vertex_map = {geom_key: i for i, geom_key in enumerate(vertex_map.keys())}
    # modify vertex indices in the faces
    faces = [ [vertex_map[geometric_key(mesh.vertex_coordinates(vkey), precision)] for vkey in mesh.face_vertices(fkey)] for mesh in meshes for fkey in mesh.faces()]

    return cls.from_vertices_and_faces(vertices, faces)

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas
