from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = [
    'mesh_substitute_vertex_in_faces'
]


def mesh_substitute_vertex_in_faces(mesh, old_vkey, new_vkey, fkeys=None):
    """Substitute in a mesh a vertex by another one.
    In all faces by default or in a given set of faces.

    Parameters
    ----------
    old_vkey : hashable
        The old vertex key.
    new_vkey : hashable
        The new vertex key.
    fkeys : list, optional
        List of face keys where to subsitute the old vertex by the new one.
        Default is to subsitute in all faces.

    Returns
    -------
    fkeys : list
        The list of modified faces.

    Examples
    --------
    >>> from compas.datastructures import Mesh
    >>> from compas.plotters import MeshPlotter
    >>> vertices = [[1.0, 0.0, 0.0], [1.0, 2.0, 0.0], [0.0, 1.0, 0.0], [2.0, 1.0, 0.0], [0.0, 0.0, 0.0]]
    >>> faces = [[0, 1, 2], [0, 3, 1]]
    >>> mesh = Mesh.from_vertices_and_faces(vertices, faces)
    >>> mesh_substitute_vertex_in_faces(mesh, 0, 4)
    >>> print(mesh.face_vertices(0), mesh.face_vertices(1))
    >>> mesh_substitute_vertex_in_faces(mesh, 4, 0, [1])
    >>> print(mesh.face_vertices(0), mesh.face_vertices(1))
    >>> plotter = MeshPlotter(mesh)
    >>> plotter.draw_vertices(text='key')
    >>> plotter.draw_edges()
    >>> plotter.draw_faces(text='key')
    >>> plotter.show()

    """

    # apply to all faces if there is none chosen
    if fkeys is None:
        fkeys = mesh.faces()

    # substitute vertices
    for fkey in fkeys:
        face_vertices = [new_vkey if key == old_vkey else key for key in mesh.face_vertices(fkey)]
        mesh.delete_face(fkey)
        mesh.add_face(face_vertices, fkey)

    return fkeys


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
