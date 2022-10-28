from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from .operations import mesh_split_face


__all__ = [
    "mesh_quads_to_triangles",
]


def mesh_quads_to_triangles(mesh, check_angles=False):
    """Convert all quadrilateral faces of a mesh to triangles by adding a diagonal edge.

    Parameters
    ----------
    mesh : :class:`~compas.datastructures.Mesh`
        A mesh data structure.
    check_angles : bool, optional
        Flag indicating that the angles of the quads should be checked to choose the best diagonal.

    Returns
    -------
    None
        The mesh is modified in place.

    """
    for fkey in list(mesh.faces()):
        attr = mesh.face_attributes(fkey)
        attr.custom_only = True
        vertices = mesh.face_vertices(fkey)
        if len(vertices) == 4:
            a, b, c, d = vertices
            t1, t2 = mesh_split_face(mesh, fkey, b, d)
            mesh.face_attributes(t1, attr.keys(), attr.values())
            mesh.face_attributes(t2, attr.keys(), attr.values())
            # mesh.facedata[t1] = attr.copy()
            # mesh.facedata[t2] = attr.copy()
            if fkey in mesh.facedata:
                del mesh.facedata[fkey]
