from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.tolerance import TOL


def mesh_delete_duplicate_vertices(mesh, precision=None):
    """Cull all duplicate vertices of a mesh and sanitize affected faces.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A mesh object.
    precision : int, optional
        Precision for converting numbers to strings.
        Default is :attr:`TOL.precision`.

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
    vertex_gkey = {}
    for vertex in mesh.vertices():
        gkey = TOL.geometric_key(mesh.vertex_attributes(vertex, "xyz"), precision=precision)
        vertex_gkey[vertex] = gkey

    gkey_vertex = {gkey: vertex for vertex, gkey in iter(vertex_gkey.items())}

    for vertex in list(mesh.vertices()):
        test = gkey_vertex[vertex_gkey[vertex]]
        if test != vertex:
            del mesh.vertex[vertex]
            del mesh.halfedge[vertex]
            for u in mesh.halfedge:
                nbrs = list(mesh.halfedge[u].keys())
                for v in nbrs:
                    if v == vertex:
                        del mesh.halfedge[u][v]

    for face in mesh.faces():
        seen = set()
        vertices = []
        for vertex in [gkey_vertex[vertex_gkey[vertex]] for vertex in mesh.face_vertices(face)]:
            if vertex not in seen:
                seen.add(vertex)
                vertices.append(vertex)
        mesh.face[face] = vertices
        for u, v in mesh.face_halfedges(face):
            mesh.halfedge[u][v] = face
            if u not in mesh.halfedge[v]:
                mesh.halfedge[v][u] = None
