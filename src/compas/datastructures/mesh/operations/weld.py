from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import pairwise

__all__ = [
    'mesh_unweld_vertices',
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
    >>>

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

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
