from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = [
    'mesh_conway_dual',
    'mesh_conway_join',
    'mesh_conway_ambo',
    'mesh_conway_kis',
    'mesh_conway_needle',
    'mesh_conway_zip',
    'mesh_conway_truncate',
    'mesh_conway_ortho',
    'mesh_conway_expand',
    'mesh_conway_gyro',
    'mesh_conway_snub',
    'mesh_conway_meta',
    'mesh_conway_bevel'
]


def mesh_conway_dual(mesh):
    """Generates the dual mesh from a seed mesh.

    Parameters
    ----------
    mesh : Mesh
        A seed mesh

    Returns
    -------
    Mesh
        The dual mesh.

    Examples
    --------
    >>> mesh = Mesh.from_polyhedron(6)
    >>> dual = mesh_conway_dual(mesh)
    >>> dual.number_of_vertices() == mesh.number_of_faces()
    True
    >>> dual.number_of_edges() == mesh.number_of_edges()
    True
    >>> dual.number_of_faces() == mesh.number_of_vertices()
    True

    References
    ----------
    Based on [1]_ and [2]_.

    .. [1] Wikipedia. *Conway polyhedron notation*.
           Available at: https://en.wikipedia.org/wiki/Conway_polyhedron_notation.
    .. [2] Hart, George. *Conway Notation for Polyhedron*.
           Available at: http://www.georgehart.com/virtual-polyhedra/conway_notation.html.
    """
    cls = type(mesh)
    vertices = [mesh.face_centroid(fkey) for fkey in mesh.faces()]
    old_faces_to_new_vertices = {fkey: i for i, fkey in enumerate(mesh.faces())}
    faces = [[old_faces_to_new_vertices[fkey] for fkey in reversed(mesh.vertex_faces(vkey, ordered=True))]
             for vkey in mesh.vertices()
             if not mesh.is_vertex_on_boundary(vkey) and len(mesh.vertex_neighbors(vkey)) != 0]
    return cls.from_vertices_and_faces(vertices, faces)


def mesh_conway_join(mesh):
    """Generates the join mesh from a seed mesh.

    Parameters
    ----------
    mesh : Mesh
        A seed mesh

    Returns
    -------
    Mesh
        The join mesh.

    Examples
    --------
    >>> mesh = Mesh.from_polyhedron(6)
    >>> join = mesh_conway_join(mesh)
    >>> join.number_of_vertices() == mesh.number_of_vertices() + mesh.number_of_faces()
    True
    >>> join.number_of_edges() == 2 * mesh.number_of_edges()
    True
    >>> join.number_of_faces() == mesh.number_of_edges()
    True

    References
    ----------
    Based on [1]_ and [2]_.

    .. [1] Wikipedia. *Conway polyhedron notation*.
           Available at: https://en.wikipedia.org/wiki/Conway_polyhedron_notation.
    .. [2] Hart, George. *Conway Notation for Polyhedron*.
           Available at: http://www.georgehart.com/virtual-polyhedra/conway_notation.html.
    """
    cls = type(mesh)
    vertices = [mesh.vertex_coordinates(vkey) for vkey in mesh.vertices()]
    vertices += [mesh.face_centroid(fkey) for fkey in mesh.faces()]
    v = mesh.number_of_vertices()
    vkey_index = {vkey: i for i, vkey in enumerate(mesh.vertices())}
    fkey_index = {fkey: i + v for i, fkey in enumerate(mesh.faces())}
    faces = [
        [vkey_index[u], fkey_index[mesh.halfedge[v][u]], vkey_index[v], fkey_index[mesh.halfedge[u][v]]]
        for u, v in mesh.edges() if not mesh.is_edge_on_boundary(u, v)]
    join_mesh = cls.from_vertices_and_faces(vertices, faces)
    # is this necessary?
    join_mesh.cull_vertices()
    return join_mesh


def mesh_conway_ambo(mesh):
    """Generates the ambo mesh from a seed mesh.

    Parameters
    ----------
    mesh : Mesh
        A seed mesh

    Returns
    -------
    mesh
        The ambo mesh.

    Examples
    --------
    >>> mesh = Mesh.from_polyhedron(6)
    >>> ambo = mesh_conway_ambo(mesh)
    >>> ambo.number_of_vertices() == mesh.number_of_edges()
    True
    >>> ambo.number_of_edges() == 2 * mesh.number_of_edges()
    True
    >>> ambo.number_of_faces() == mesh.number_of_vertices() + mesh.number_of_faces()
    True

    References
    ----------
    Based on [1]_ and [2]_.

    .. [1] Wikipedia. *Conway polyhedron notation*.
           Available at: https://en.wikipedia.org/wiki/Conway_polyhedron_notation.
    .. [2] Hart, George. *Conway Notation for Polyhedron*.
           Available at: http://www.georgehart.com/virtual-polyhedra/conway_notation.html.
    """
    return mesh_conway_dual(mesh_conway_join(mesh))


def mesh_conway_kis(mesh):
    """Generates the kis mesh from a seed mesh.

    Parameters
    ----------
    mesh : Mesh
        A seed mesh

    Returns
    -------
    mesh
        The kis mesh.

    Examples
    --------
    >>> mesh = Mesh.from_polyhedron(6)
    >>> kis = mesh_conway_kis(mesh)
    >>> kis.number_of_vertices() == mesh.number_of_vertices() + mesh.number_of_faces()
    True
    >>> kis.number_of_edges() == 3 * mesh.number_of_edges()
    True
    >>> kis.number_of_faces() == 2 * mesh.number_of_edges()
    True

    References
    ----------
    Based on [1]_ and [2]_.

    .. [1] Wikipedia. *Conway polyhedron notation*.
           Available at: https://en.wikipedia.org/wiki/Conway_polyhedron_notation.
    .. [2] Hart, George. *Conway Notation for Polyhedron*.
           Available at: http://www.georgehart.com/virtual-polyhedra/conway_notation.html.
    """
    cls = type(mesh)
    vertices = [mesh.vertex_coordinates(vkey) for vkey in mesh.vertices()]
    vertices += [mesh.face_centroid(fkey) for fkey in mesh.faces()]
    v = mesh.number_of_vertices()
    vkey_index = {vkey: i for i, vkey in enumerate(mesh.vertices())}
    fkey_index = {fkey: i + v for i, fkey in enumerate(mesh.faces())}
    faces = [
        [vkey_index[u], vkey_index[v], fkey_index[mesh.halfedge[u][v]]]
        for fkey in mesh.faces() for u, v in mesh.face_halfedges(fkey)]
    return cls.from_vertices_and_faces(vertices, faces)


def mesh_conway_needle(mesh):
    """Generates the needle mesh from a seed mesh.

    Parameters
    ----------
    mesh : Mesh
        A seed mesh

    Returns
    -------
    mesh
        The needle mesh.

    Examples
    --------
    >>> mesh = Mesh.from_polyhedron(6)
    >>> needle = mesh_conway_needle(mesh)
    >>> needle.number_of_vertices() == mesh.number_of_vertices() + mesh.number_of_faces()
    True
    >>> needle.number_of_edges() == 3 * mesh.number_of_edges()
    True
    >>> needle.number_of_faces() == 2 * mesh.number_of_edges()
    True

    References
    ----------
    Based on [1]_ and [2]_.

    .. [1] Wikipedia. *Conway polyhedron notation*.
           Available at: https://en.wikipedia.org/wiki/Conway_polyhedron_notation.
    .. [2] Hart, George. *Conway Notation for Polyhedron*.
           Available at: http://www.georgehart.com/virtual-polyhedra/conway_notation.html.
    """
    return mesh_conway_kis(mesh_conway_dual(mesh))


def mesh_conway_zip(mesh):
    """Generates the zip mesh from a seed mesh.

    Parameters
    ----------
    mesh : Mesh
        A seed mesh

    Returns
    -------
    mesh
        The zip mesh.

    Examples
    --------
    >>> mesh = Mesh.from_polyhedron(6)
    >>> zipp = mesh_conway_zip(mesh)
    >>> zipp.number_of_vertices() == 2 * mesh.number_of_edges()
    True
    >>> zipp.number_of_edges() == 3 * mesh.number_of_edges()
    True
    >>> zipp.number_of_faces() == mesh.number_of_vertices() + mesh.number_of_faces()
    True

    References
    ----------
    Based on [1]_ and [2]_.

    .. [1] Wikipedia. *Conway polyhedron notation*.
           Available at: https://en.wikipedia.org/wiki/Conway_polyhedron_notation.
    .. [2] Hart, George. *Conway Notation for Polyhedron*.
           Available at: http://www.georgehart.com/virtual-polyhedra/conway_notation.html.

    """
    return mesh_conway_dual(mesh_conway_kis(mesh))


def mesh_conway_truncate(mesh):
    """Generates the truncate mesh from a seed mesh.

    Parameters
    ----------
    mesh : Mesh
        A seed mesh

    Returns
    -------
    mesh
        The truncate mesh.

    Examples
    --------
    >>> mesh = Mesh.from_polyhedron(6)
    >>> trun = mesh_conway_truncate(mesh)
    >>> trun.number_of_vertices() == 2 * mesh.number_of_edges()
    True
    >>> trun.number_of_edges() == 3 * mesh.number_of_edges()
    True
    >>> trun.number_of_faces() == mesh.number_of_vertices() + mesh.number_of_faces()
    True

    References
    ----------
    Based on [1]_ and [2]_.

    .. [1] Wikipedia. *Conway polyhedron notation*.
           Available at: https://en.wikipedia.org/wiki/Conway_polyhedron_notation.
    .. [2] Hart, George. *Conway Notation for Polyhedron*.
           Available at: http://www.georgehart.com/virtual-polyhedra/conway_notation.html.
    """
    # same as conway_dual(conway_needle())?
    return mesh_conway_dual(mesh_conway_kis(mesh_conway_dual(mesh)))


def mesh_conway_ortho(mesh):
    """Generates the ortho mesh from a seed mesh.

    Parameters
    ----------
    mesh : Mesh
        A seed mesh

    Returns
    -------
    mesh
        The ortho mesh.

    Examples
    --------
    >>> mesh = Mesh.from_polyhedron(6)
    >>> orth = mesh_conway_ortho(mesh)
    >>> orth.number_of_vertices() == mesh.number_of_vertices() + mesh.number_of_faces() + mesh.number_of_edges()
    True
    >>> orth.number_of_edges() == 4 * mesh.number_of_edges()
    True
    >>> orth.number_of_faces() == 2 * mesh.number_of_edges()
    True

    References
    ----------
    Based on [1]_ and [2]_.

    .. [1] Wikipedia. *Conway polyhedron notation*.
           Available at: https://en.wikipedia.org/wiki/Conway_polyhedron_notation.
    .. [2] Hart, George. *Conway Notation for Polyhedron*.
           Available at: http://www.georgehart.com/virtual-polyhedra/conway_notation.html.
    """
    return mesh_conway_join(mesh_conway_join(mesh))


def mesh_conway_expand(mesh):
    """Generates the expand mesh from a seed mesh.

    Parameters
    ----------
    mesh : Mesh
        A seed mesh

    Returns
    -------
    mesh
        The expand mesh.

    Examples
    --------
    >>> mesh = Mesh.from_polyhedron(6)
    >>> expa = mesh_conway_expand(mesh)
    >>> expa.number_of_vertices() == 2 * mesh.number_of_edges()
    True
    >>> expa.number_of_edges() == 4 * mesh.number_of_edges()
    True
    >>> expa.number_of_faces() == mesh.number_of_vertices() + mesh.number_of_faces() + mesh.number_of_edges()
    True

    References
    ----------
    Based on [1]_ and [2]_.

    .. [1] Wikipedia. *Conway polyhedron notation*.
           Available at: https://en.wikipedia.org/wiki/Conway_polyhedron_notation.
    .. [2] Hart, George. *Conway Notation for Polyhedron*.
           Available at: http://www.georgehart.com/virtual-polyhedra/conway_notation.html.
    """
    return mesh_conway_ambo(mesh_conway_ambo(mesh))


def mesh_conway_gyro(mesh):
    """Generates the gyro mesh from a seed mesh.

    Parameters
    ----------
    mesh : Mesh
        A seed mesh

    Returns
    -------
    mesh
        The gyro mesh.

    Examples
    --------
    >>> mesh = Mesh.from_polyhedron(6)
    >>> gyro = mesh_conway_gyro(mesh)
    >>> gyro.number_of_vertices() == mesh.number_of_vertices() + mesh.number_of_faces() + 2 * mesh.number_of_edges()
    True
    >>> gyro.number_of_edges() == 5 * mesh.number_of_edges()
    True
    >>> gyro.number_of_faces() == 2 * mesh.number_of_edges()
    True

    References
    ----------
    Based on [1]_ and [2]_.

    .. [1] Wikipedia. *Conway polyhedron notation*.
           Available at: https://en.wikipedia.org/wiki/Conway_polyhedron_notation.
    .. [2] Hart, George. *Conway Notation for Polyhedron*.
           Available at: http://www.georgehart.com/virtual-polyhedra/conway_notation.html.
    """
    cls = type(mesh)
    vertices = [mesh.vertex_coordinates(vkey) for vkey in mesh.vertices()]
    vertices += [mesh.face_centroid(fkey) for fkey in mesh.faces()]
    vertices += [mesh.edge_point(u, v, t=.33) for u in mesh.vertices() for v in mesh.halfedge[u]]
    V = mesh.number_of_vertices()
    F = mesh.number_of_faces()
    vkey_index = {vkey: i for i, vkey in enumerate(mesh.vertices())}
    fkey_index = {fkey: i + V for i, fkey in enumerate(mesh.faces())}
    ekey_index = {halfedge: i + V + F for i, halfedge in enumerate([(u, v) for u in mesh.vertices() for v in mesh.halfedge[u]])}
    faces = []
    for fkey in mesh.faces():
        for u, v in mesh.face_halfedges(fkey):
            faces.append([
                ekey_index[u, v],
                ekey_index[v, u],
                vkey_index[v],
                ekey_index[v, mesh.face_vertex_descendant(fkey, v)],
                fkey_index[mesh.halfedge[u][v]]])
    return cls.from_vertices_and_faces(vertices, faces)


def mesh_conway_snub(mesh):
    """Generates the snub mesh from a seed mesh.

    Parameters
    ----------
    mesh : Mesh
        A seed mesh

    Returns
    -------
    mesh
        The gyro mesh.

    Examples
    --------
    >>> mesh = Mesh.from_polyhedron(6)
    >>> snub = mesh_conway_snub(mesh)
    >>> snub.number_of_vertices() == 2 * mesh.number_of_edges()
    True
    >>> snub.number_of_edges() == 5 * mesh.number_of_edges()
    True
    >>> snub.number_of_faces() == mesh.number_of_vertices() + mesh.number_of_faces() + 2 * mesh.number_of_edges()
    True

    References
    ----------
    Based on [1]_ and [2]_.

    .. [1] Wikipedia. *Conway polyhedron notation*.
           Available at: https://en.wikipedia.org/wiki/Conway_polyhedron_notation.
    .. [2] Hart, George. *Conway Notation for Polyhedron*.
           Available at: http://www.georgehart.com/virtual-polyhedra/conway_notation.html.
    """
    return mesh_conway_dual(mesh_conway_gyro(mesh_conway_dual(mesh)))


def mesh_conway_meta(mesh):
    """Generates the meta mesh from a seed mesh.

    Parameters
    ----------
    mesh : Mesh
        A seed mesh

    Returns
    -------
    mesh
        The meta mesh.

    Examples
    --------
    >>> mesh = Mesh.from_polyhedron(6)
    >>> meta = mesh_conway_meta(mesh)
    >>> meta.number_of_vertices() == mesh.number_of_vertices() + mesh.number_of_faces() + mesh.number_of_edges()
    True
    >>> meta.number_of_edges() == 6 * mesh.number_of_edges()
    True
    >>> meta.number_of_faces() == 4 * mesh.number_of_edges()
    True

    References
    ----------
    Based on [1]_ and [2]_.

    .. [1] Wikipedia. *Conway polyhedron notation*.
           Available at: https://en.wikipedia.org/wiki/Conway_polyhedron_notation.
    .. [2] Hart, George. *Conway Notation for Polyhedron*.
           Available at: http://www.georgehart.com/virtual-polyhedra/conway_notation.html.
    """
    return mesh_conway_kis(mesh_conway_join(mesh))


def mesh_conway_bevel(mesh):
    """Generates the bevel mesh from a seed mesh.

    Parameters
    ----------
    mesh : Mesh
        A seed mesh

    Returns
    -------
    mesh
        The bevel mesh.

    Examples
    --------
    >>> mesh = Mesh.from_polyhedron(6)
    >>> bevl = mesh_conway_bevel(mesh)
    >>> bevl.number_of_vertices() == 4 * mesh.number_of_edges()
    True
    >>> bevl.number_of_edges() == 6 * mesh.number_of_edges()
    True
    >>> bevl.number_of_faces() == mesh.number_of_vertices() + mesh.number_of_faces() + mesh.number_of_edges()
    True

    References
    ----------
    Based on [1]_ and [2]_.

    .. [1] Wikipedia. *Conway polyhedron notation*.
           Available at: https://en.wikipedia.org/wiki/Conway_polyhedron_notation.
    .. [2] Hart, George. *Conway Notation for Polyhedron*.
           Available at: http://www.georgehart.com/virtual-polyhedra/conway_notation.html.
    """
    return mesh_conway_truncate(mesh_conway_ambo(mesh))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest
    from compas.datastructures import Mesh  # noqa: F401

    doctest.testmod(globs=globals())
