from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = [
    'conway_dual',
    'conway_join',
    'conway_ambo',
    'conway_kis',
    'conway_needle',
    'conway_zip',
    'conway_truncate',
    'conway_ortho',
    'conway_expand',
    'conway_gyro',
    'conway_snub',
    'conway_meta',
    'conway_bevel'
]


def conway_dual(mesh):
    """Generates the dual mesh from a seed mesh.

    Parameters
    ----------
    mesh : Mesh
        A seed mesh

    Returns
    -------
    mesh
        The dual mesh.

    References
    ----------
    .. [1] Wikipedia. *Conway polyhedron notation*.
           Available at: https://en.wikipedia.org/wiki/Conway_polyhedron_notation.
    .. [2] Hart, George. *Conway Notation for Polyhedron*.
           Available at: http://www.georgehart.com/virtual-polyhedra/conway_notation.html.

    """
    cls = type(mesh)

    vertices = [mesh.face_centroid(fkey) for fkey in mesh.faces()]

    old_faces_to_new_vertices = {fkey: i for i, fkey in enumerate(mesh.faces())}

    faces = [[old_faces_to_new_vertices[fkey] for fkey in reversed(mesh.vertex_faces(vkey, ordered = True))] for vkey in mesh.vertices() if not mesh.is_vertex_on_boundary(vkey) and len(mesh.vertex_neighbors(vkey)) != 0]

    return cls.from_vertices_and_faces(vertices, faces)


def conway_join(mesh):
    """Generates the join mesh from a seed mesh.

    Parameters
    ----------
    mesh : Mesh
        A seed mesh

    Returns
    -------
    join_mesh : mesh
        The join mesh.

    References
    ----------
    .. [1] Wikipedia. *Conway polyhedron notation*.
           Available at: https://en.wikipedia.org/wiki/Conway_polyhedron_notation.
    .. [2] Hart, George. *Conway Notation for Polyhedron*.
           Available at: http://www.georgehart.com/virtual-polyhedra/conway_notation.html.

    """
    mesh_class = type(mesh)

    vertices = [mesh.vertex_coordinates(vkey) for vkey in mesh.vertices()] + [mesh.face_centroid(fkey) for fkey in mesh.faces()]

    old_vertices_to_new_vertices = {vkey: i for i, vkey in enumerate(mesh.vertices())}
    old_faces_to_new_vertices = {fkey: i + mesh.number_of_vertices() for i, fkey in enumerate(mesh.faces())}

    faces = [[
        old_vertices_to_new_vertices[u], old_faces_to_new_vertices[mesh.halfedge[v][u]], old_vertices_to_new_vertices[v], old_faces_to_new_vertices[mesh.halfedge[u][v]]
        ] for u, v in mesh.edges() if not mesh.is_edge_on_boundary(u, v)]

    join_mesh =  mesh_class.from_vertices_and_faces(vertices, faces)
    join_mesh.cull_vertices()

    return join_mesh


def conway_ambo(mesh):
    """Generates the ambo mesh from a seed mesh.

    Parameters
    ----------
    mesh : Mesh
        A seed mesh

    Returns
    -------
    mesh
        The ambo mesh.

    References
    ----------
    .. [1] Wikipedia. *Conway polyhedron notation*.
           Available at: https://en.wikipedia.org/wiki/Conway_polyhedron_notation.
    .. [2] Hart, George. *Conway Notation for Polyhedron*.
           Available at: http://www.georgehart.com/virtual-polyhedra/conway_notation.html.

    """
    return conway_dual(conway_join(mesh))


def conway_kis(mesh):
    """Generates the kis mesh from a seed mesh.

    Parameters
    ----------
    mesh : Mesh
        A seed mesh

    Returns
    -------
    mesh
        The kis mesh.

    References
    ----------
    .. [1] Wikipedia. *Conway polyhedron notation*.
           Available at: https://en.wikipedia.org/wiki/Conway_polyhedron_notation.
    .. [2] Hart, George. *Conway Notation for Polyhedron*.
           Available at: http://www.georgehart.com/virtual-polyhedra/conway_notation.html.

    """
    mesh_class = type(mesh)

    vertices = [mesh.vertex_coordinates(vkey) for vkey in mesh.vertices()] + [mesh.face_centroid(fkey) for fkey in mesh.faces()]

    old_vertices_to_new_vertices = {vkey: i for i, vkey in enumerate(mesh.vertices())}
    old_faces_to_new_vertices = {fkey: i + mesh.number_of_vertices() for i, fkey in enumerate(mesh.faces())}

    faces = [[
        old_vertices_to_new_vertices[u], old_vertices_to_new_vertices[v], old_faces_to_new_vertices[mesh.halfedge[u][v]]
        ] for fkey in mesh.faces() for u, v in mesh.face_halfedges(fkey)]

    return mesh_class.from_vertices_and_faces(vertices, faces)


def conway_needle(mesh):
    """Generates the needle mesh from a seed mesh.

    Parameters
    ----------
    mesh : Mesh
        A seed mesh

    Returns
    -------
    mesh
        The needle mesh.

    References
    ----------
    .. [1] Wikipedia. *Conway polyhedron notation*.
           Available at: https://en.wikipedia.org/wiki/Conway_polyhedron_notation.
    .. [2] Hart, George. *Conway Notation for Polyhedron*.
           Available at: http://www.georgehart.com/virtual-polyhedra/conway_notation.html.

    """
    return conway_kis(conway_dual(mesh))


def conway_zip(mesh):
    """Generates the zip mesh from a seed mesh.

    Parameters
    ----------
    mesh : Mesh
        A seed mesh

    Returns
    -------
    mesh
        The zip mesh.

    References
    ----------
    .. [1] Wikipedia. *Conway polyhedron notation*.
           Available at: https://en.wikipedia.org/wiki/Conway_polyhedron_notation.
    .. [2] Hart, George. *Conway Notation for Polyhedron*.
           Available at: http://www.georgehart.com/virtual-polyhedra/conway_notation.html.

    """
    return conway_dual(conway_kis(mesh))


def conway_truncate(mesh):
    """Generates the truncate mesh from a seed mesh.

    Parameters
    ----------
    mesh : Mesh
        A seed mesh

    Returns
    -------
    mesh
        The truncate mesh.

    References
    ----------
    .. [1] Wikipedia. *Conway polyhedron notation*.
           Available at: https://en.wikipedia.org/wiki/Conway_polyhedron_notation.
    .. [2] Hart, George. *Conway Notation for Polyhedron*.
           Available at: http://www.georgehart.com/virtual-polyhedra/conway_notation.html.

    """
    return conway_dual(conway_kis(conway_dual(mesh)))


def conway_ortho(mesh):
    """Generates the ortho mesh from a seed mesh.

    Parameters
    ----------
    mesh : Mesh
        A seed mesh

    Returns
    -------
    mesh
        The ortho mesh.

    References
    ----------
    .. [1] Wikipedia. *Conway polyhedron notation*.
           Available at: https://en.wikipedia.org/wiki/Conway_polyhedron_notation.
    .. [2] Hart, George. *Conway Notation for Polyhedron*.
           Available at: http://www.georgehart.com/virtual-polyhedra/conway_notation.html.

    """
    return conway_join(conway_join(mesh))


def conway_expand(mesh):
    """Generates the expand mesh from a seed mesh.

    Parameters
    ----------
    mesh : Mesh
        A seed mesh

    Returns
    -------
    mesh
        The expand mesh.

    References
    ----------
    .. [1] Wikipedia. *Conway polyhedron notation*.
           Available at: https://en.wikipedia.org/wiki/Conway_polyhedron_notation.
    .. [2] Hart, George. *Conway Notation for Polyhedron*.
           Available at: http://www.georgehart.com/virtual-polyhedra/conway_notation.html.

    """
    return conway_ambo(conway_ambo(mesh))


def conway_gyro(mesh):
    """Generates the gyro mesh from a seed mesh.

    Parameters
    ----------
    mesh : Mesh
        A seed mesh

    Returns
    -------
    mesh
        The gyro mesh.

    References
    ----------
    .. [1] Wikipedia. *Conway polyhedron notation*.
           Available at: https://en.wikipedia.org/wiki/Conway_polyhedron_notation.
    .. [2] Hart, George. *Conway Notation for Polyhedron*.
           Available at: http://www.georgehart.com/virtual-polyhedra/conway_notation.html.

    """
    mesh_class = type(mesh)

    vertices = [mesh.vertex_coordinates(vkey) for vkey in mesh.vertices()] + [mesh.face_centroid(fkey) for fkey in mesh.faces()] + [mesh.edge_point(u, v, t = .33) for u in mesh.vertices() for v in mesh.halfedge[u]]

    old_vertices_to_new_vertices = {vkey: i for i, vkey in enumerate(mesh.vertices())}
    old_faces_to_new_vertices = {fkey: i + mesh.number_of_vertices() for i, fkey in enumerate(mesh.faces())}
    old_halfedges_to_new_vertices = {halfedge: i + mesh.number_of_vertices() + mesh.number_of_faces() for i, halfedge in enumerate([(u, v) for u in mesh.vertices() for v in mesh.halfedge[u]])}

    faces = []
    for fkey in mesh.faces():
        for u, v in mesh.face_halfedges(fkey):
            faces.append([
                old_halfedges_to_new_vertices[(u, v)],
                old_halfedges_to_new_vertices[(v, u)],
                old_vertices_to_new_vertices[v],
                old_halfedges_to_new_vertices[(v, mesh.face_vertex_descendant(fkey, v))],
                old_faces_to_new_vertices[mesh.halfedge[u][v]]
            ])

    return mesh_class.from_vertices_and_faces(vertices, faces)


def conway_snub(mesh):
    """Generates the snub mesh from a seed mesh.

    Parameters
    ----------
    mesh : Mesh
        A seed mesh

    Returns
    -------
    mesh
        The gyro mesh.

    References
    ----------
    .. [1] Wikipedia. *Conway polyhedron notation*.
           Available at: https://en.wikipedia.org/wiki/Conway_polyhedron_notation.
    .. [2] Hart, George. *Conway Notation for Polyhedron*.
           Available at: http://www.georgehart.com/virtual-polyhedra/conway_notation.html.

    """
    return conway_dual(conway_gyro(conway_dual(mesh)))


def conway_meta(mesh):
    """Generates the meta mesh from a seed mesh.

    Parameters
    ----------
    mesh : Mesh
        A seed mesh

    Returns
    -------
    mesh
        The meta mesh.

    References
    ----------
    .. [1] Wikipedia. *Conway polyhedron notation*.
           Available at: https://en.wikipedia.org/wiki/Conway_polyhedron_notation.
    .. [2] Hart, George. *Conway Notation for Polyhedron*.
           Available at: http://www.georgehart.com/virtual-polyhedra/conway_notation.html.

    """
    return conway_kis(conway_join(mesh))


def conway_bevel(mesh):
    """Generates the bevel mesh from a seed mesh.

    Parameters
    ----------
    mesh : Mesh
        A seed mesh

    Returns
    -------
    mesh
        The bevel mesh.

    References
    ----------
    .. [1] Wikipedia. *Conway polyhedron notation*.
           Available at: https://en.wikipedia.org/wiki/Conway_polyhedron_notation.
    .. [2] Hart, George. *Conway Notation for Polyhedron*.
           Available at: http://www.georgehart.com/virtual-polyhedra/conway_notation.html.

    """
    return conway_truncate(conway_ambo(mesh))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import compas
