from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import geometric_key


__all__ = ["mesh_delete_duplicate_vertices"]


def mesh_delete_duplicate_vertices(mesh, precision=None):
    """Cull all duplicate vertices of a mesh and sanitize affected faces.

    Parameters
    ----------
    mesh : :class:`~compas.datastructures.Mesh`
        A mesh object.
    precision : str, optional
        Precision for point comparison in the form of a string formatting specifier.
        For example, floating point precision (``'3f'``), or decimal integer (``'d'``).
        Default is :attr:`compas.PRECISION`.

    Returns
    -------
    None
        The mesh is modified in-place.

    Examples
    --------
    >>> import compas
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_obj(compas.get('faces.obj'))
    >>> mesh.number_of_vertices()
    36
    >>> for x, y, z in mesh.vertices_attributes('xyz', keys=list(mesh.vertices())[:5]):
    ...     mesh.add_vertex(x=x, y=y, z=z)
    ...
    36
    37
    38
    39
    40
    >>> mesh.number_of_vertices()
    41
    >>> mesh_delete_duplicate_vertices(mesh)
    >>> mesh.number_of_vertices()
    36

    """
    key_gkey = {key: geometric_key(mesh.vertex_attributes(key, "xyz"), precision=precision) for key in mesh.vertices()}
    gkey_key = {gkey: key for key, gkey in iter(key_gkey.items())}

    for key in list(mesh.vertices()):
        test = gkey_key[key_gkey[key]]
        if test != key:
            del mesh.vertex[key]
            del mesh.halfedge[key]
            for u in mesh.halfedge:
                nbrs = list(mesh.halfedge[u].keys())
                for v in nbrs:
                    if v == key:
                        del mesh.halfedge[u][v]

    for fkey in mesh.faces():
        seen = set()
        face = []
        for key in [gkey_key[key_gkey[key]] for key in mesh.face_vertices(fkey)]:
            if key not in seen:
                seen.add(key)
                face.append(key)
        mesh.face[fkey] = face
        for u, v in mesh.face_halfedges(fkey):
            mesh.halfedge[u][v] = fkey
            if u not in mesh.halfedge[v]:
                mesh.halfedge[v][u] = None
