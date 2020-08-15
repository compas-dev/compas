from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import pi


__all__ = ['mesh_dual']


PI2 = 2.0 * pi


def mesh_dual(mesh, cls=None):
    """Construct the dual of a mesh.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.
    cls : Mesh, optional [None]
        The type of the dual mesh.
        Defaults to the type of the provided mesh object.

    Returns
    -------
    Mesh
        The dual mesh object.

    Examples
    --------
    >>>

    """
    if not cls:
        cls = type(mesh)

    dual = cls()

    face_centroid = {face: mesh.face_centroid(face) for face in mesh.faces()}
    inner = list(set(mesh.vertices()) - set(mesh.vertices_on_boundary()))
    vertex_xyz = {}
    face_vertices = {}

    for vertex in inner:
        faces = mesh.vertex_faces(vertex, ordered=True)
        for face in faces:
            if face not in vertex_xyz:
                vertex_xyz[face] = face_centroid[face]
        face_vertices[vertex] = faces

    for vertex in vertex_xyz:
        x, y, z = vertex_xyz[vertex]
        dual.add_vertex(vertex, x=x, y=y, z=z)

    for face in face_vertices:
        dual.add_face(face_vertices[face], fkey=face)

    return dual


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    # import compas
    # from compas.datastructures import Mesh
    # from compas_plotters import MeshPlotter

    # mesh = Mesh.from_obj(compas.get('faces.obj'))
    # plotter = MeshPlotter(mesh_dual(mesh), figsize=(8, 5))
    # plotter.draw_edges()
    # plotter.draw_vertices()
    # plotter.show()

    import doctest
    doctest.testmod(globs=globals())
