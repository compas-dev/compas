from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import copy

from compas.utilities import pairwise

from compas.utilities import geometric_key
from compas.utilities import reverse_geometric_key

__all__ = [
    'mesh_unweld_vertices',
    'weld_mesh',
    'join_meshes',
    'join_and_weld_meshes',
]

def mesh_unweld_vertices(mesh, fkey, where=None):
    """Unweld a face of the mesh.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.
    fkey : hashable
        The identifier of a face.
    where : list (None)
        A list of vertices to unweld.
        Default is to unweld all vertices of the face.

    Examples
    --------
    .. plot::
        :include-source:

        import compas

        from compas.datastructures import Mesh
        from compas.plotters import MeshPlotter
        from compas.geometry import subtract_vectors

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        vertices = set(mesh.vertices())

        fkey  = 12
        where = mesh.face_vertices(fkey)[0:1]
        centroid = mesh.face_centroid(fkey)

        face = mesh.unweld_vertices(fkey, where)

        for key in face:
            if key in vertices:
                continue
            xyz = mesh.vertex_coordinates(key)
            v = subtract_vectors(centroid, xyz)
            mesh.vertex[key]['x'] += 0.3 * v[0]
            mesh.vertex[key]['y'] += 0.3 * v[1]
            mesh.vertex[key]['z'] += 0.3 * v[2]

        plotter = MeshPlotter(mesh, figsize=(10, 7))

        plotter.draw_vertices()
        plotter.draw_faces(text={fkey: fkey for fkey in mesh.faces()})

        plotter.show()

    """
    face = []
    vertices = mesh.face_vertices(fkey)

    if not where:
        where = vertices

    for u, v in pairwise(vertices + vertices[0:1]):
        if u in where:
            x, y, z = mesh.vertex_coordinates(u)
            u = mesh.add_vertex(x=x, y=y, z=z)
        if u in where or v in where:
            mesh.halfedge[v][u] = None
        face.append(u)

    mesh.add_face(face, fkey=fkey)

    return face

def mesh_weld(mesh, precision = None):
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

    # create vertex map based on geometric keys in dictionary without duplicates
    vertex_map = {geometric_key(mesh.vertex_coordinates(vkey), precision): vkey for vkey in mesh.vertices()}
    # list vertices with coordinates
    vertices = [reverse_geometric_key(geom_key) for geom_key in vertex_map.keys()]
    # reorder vertex keys in vertex map
    vertex_map = {geom_key: i for i, geom_key in enumerate(vertex_map.keys())}
    # modify vertex indices in the faces
    faces = [ [vertex_map[geometric_key(mesh.vertex_coordinates(vkey), precision)] for vkey in mesh.face_vertices(fkey)] for fkey in mesh.faces()]

    return Mesh.from_vertices_and_faces(vertices, faces)

def meshes_join_and_weld(meshes, precision = None):
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

    # create vertex map based on geometric keys in dictionary without duplicates
    vertex_map = {geometric_key(mesh.vertex_coordinates(vkey), precision): vkey for mesh in meshes for vkey in mesh.vertices()}
    # list vertices with coordinates
    vertices = [reverse_geometric_key(geom_key) for geom_key in vertex_map.keys()]
    # reorder vertex keys in vertex map
    vertex_map = {geom_key: i for i, geom_key in enumerate(vertex_map.keys())}
    # modify vertex indices in the faces
    faces = [ [vertex_map[geometric_key(mesh.vertex_coordinates(vkey), precision)] for vkey in mesh.face_vertices(fkey)] for mesh in meshes for fkey in mesh.faces()]

    return Mesh.from_vertices_and_faces(vertices, faces)

def meshes_join(meshes):
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

    vertices = []
    faces = []

    for mesh in meshes:
        # create vertex map based on geometric keys in dictionary with duplicates
        vertex_map = ({vkey: len(vertices) + i for i, vkey in enumerate(mesh.vertices())})
        # list vertices with coordinates
        vertices += [mesh.vertex_coordinates(vkey) for vkey in mesh.vertices()]
        # modify vertex indices in the faces
        faces += [ [vertex_map[vkey] for vkey in mesh.face_vertices(fkey)] for fkey in mesh.faces()]

    return Mesh.from_vertices_and_faces(vertices, faces)

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures import Mesh
    from compas.plotters import MeshPlotter
    from compas.geometry import subtract_vectors

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    vertices = set(mesh.vertices())

    fkey  = 12
    where = mesh.face_vertices(fkey)[0:2]
    centroid = mesh.face_centroid(fkey)

    face = mesh.unweld_vertices(fkey, where)

    for key in face:
        if key in vertices:
            continue
        xyz = mesh.vertex_coordinates(key)
        v = subtract_vectors(centroid, xyz)
        mesh.vertex[key]['x'] += 0.3 * v[0]
        mesh.vertex[key]['y'] += 0.3 * v[1]
        mesh.vertex[key]['z'] += 0.3 * v[2]

    plotter = MeshPlotter(mesh, figsize=(10, 7))

    plotter.draw_vertices()
    plotter.draw_faces(text={fkey: fkey for fkey in mesh.faces()})

    plotter.show()