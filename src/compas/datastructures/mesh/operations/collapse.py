from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = [
    'mesh_collapse_edge',
    'trimesh_collapse_edge',
]


def is_collapse_legal(mesh, u, v, allow_boundary=False):
    """Verify if the requested collapse is legal for a triangle mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        The mesh.
    u : str
        The vertex to collapse towards.
    v : str
        The vertex to collapse.

    Returns
    -------
    bool
        `True` if the collapse is legal.
        `False` otherwise.

    """
    u_on = mesh.is_vertex_on_boundary(u)
    v_on = mesh.is_vertex_on_boundary(v)

    if v_on and not u_on:
        return False

    # collapsing of boundary vertices is currently not supported
    # change this to `and` to support collapsing to or from the boundary
    if not allow_boundary:
        if u_on or v_on:
            return False

    fkey_uv = mesh.halfedge[u][v]
    fkey_vu = mesh.halfedge[v][u]

    # check for contained faces
    for nbr in mesh.halfedge[u]:
        if nbr in mesh.halfedge[v]:
            fkey_nbr_v = mesh.halfedge[nbr][v]
            fkey_u_nbr = mesh.halfedge[u][nbr]

            if fkey_nbr_v is None and fkey_u_nbr is None:
                return False

            # in a trimesh
            # u and v should have one neighbor in common
            # and uv-nbr or vu-nbr
            # should define a face
            # check if UV > NBR is a face
            if mesh.halfedge[v][nbr] == fkey_uv and mesh.halfedge[nbr][u] != fkey_uv:
                return False
            # check if VU > NBR is a face
            if mesh.halfedge[u][nbr] == fkey_vu and mesh.halfedge[nbr][v] != fkey_vu:
                return False

    for nbr in mesh.halfedge[v]:
        if nbr in mesh.halfedge[u]:
            # check if UV > NBR is a face
            if mesh.halfedge[v][nbr] == fkey_uv and mesh.halfedge[nbr][u] != fkey_uv:
                return False
            # check if V > U > NBR is a face
            if mesh.halfedge[u][nbr] == fkey_vu and mesh.halfedge[nbr][v] != fkey_vu:
                return False

    return True


def mesh_collapse_edge(mesh, u, v, t=0.5, allow_boundary=False, fixed=None):
    """Collapse an edge to its first or second vertex, or to an intermediate
    point.

    Notes:
        An edge can only be collapsed if the collapse is `legal`. A collapse is
        legal if it meets the following requirements:

            * any vertex `w` that is a neighbor of both `u` and `v` is a face
              of the mesh
            * `u` and `v` are not on the boundary
            * ...

        See [] for a detailed explanation of these requirements.

    Parameters:
        u (str): The first vertex of the (half-) edge.
        v (str): The second vertex of the (half-) edge.
        t (float): Determines where to collapse to. If `t == 0.0` collapse
            to `u`. If `t == 1.0` collapse to `v`. If `0.0 < t < 1.0`,
            collapse to a point between `u` and `v`.

    Returns:
        None

    Raises:
        ValueError: If `u` and `v` are not neighbors.

    """
    if t < 0.0:
        raise ValueError('Parameter t should be greater than or equal to 0.')
    if t > 1.0:
        raise ValueError('Parameter t should be smaller than or equal to 1.')

    # check collapse conditions
    if not is_collapse_legal(mesh, u, v, allow_boundary=allow_boundary):
        return False

    # compare to fixed
    fixed = fixed or []
    if v in fixed or u in fixed:
        return False

    # move U
    x, y, z = mesh.edge_point(u, v, t)
    mesh.vertex[u]['x'] = x
    mesh.vertex[u]['y'] = y
    mesh.vertex[u]['z'] = z

    # UV face
    fkey = mesh.halfedge[u][v]

    if fkey is None:
        del mesh.halfedge[u][v]

    else:
        face = mesh.face_vertices(fkey)
        f = len(face)

        # switch between UV face sizes
        # note: in a trimesh this is not necessary!
        if f < 3:
            raise Exception("Invalid mesh face: {}".format(fkey))
        if f == 3:
            # delete UV
            o = face[face.index(u) - 1]
            del mesh.halfedge[u][v]
            del mesh.halfedge[v][o]
            del mesh.halfedge[o][u]
            del mesh.face[fkey]
        else:
            # u > v > d => u > d
            d = mesh.face_vertex_descendant(fkey, v)
            face.remove(v)
            del mesh.halfedge[u][v]
            del mesh.halfedge[v][d]
            mesh.halfedge[u][d] = fkey

    # VU face
    fkey = mesh.halfedge[v][u]

    if fkey is None:
        del mesh.halfedge[v][u]

    else:
        face = mesh.face_vertices(fkey)
        f = len(face)

        # switch between VU face sizes
        # note: in a trimesh this is not necessary!
        if f < 3:
            raise Exception("Invalid mesh face: {}".format(fkey))
        if f == 3:
            # delete UV
            o = face[face.index(v) - 1]
            del mesh.halfedge[v][u]  # the collapsing halfedge
            del mesh.halfedge[u][o]
            del mesh.halfedge[o][v]
            del mesh.face[fkey]
        else:
            # a > v > u => a > u
            a = mesh.face_vertex_ancestor(fkey, v)
            face.remove(v)
            del mesh.halfedge[a][v]
            del mesh.halfedge[v][u]
            mesh.halfedge[a][u] = fkey

    # V neighbors and halfedges coming into V
    for nbr, fkey in list(mesh.halfedge[v].items()):

        if fkey is None:
            mesh.halfedge[u][nbr] = None
            del mesh.halfedge[v][nbr]
        else:
            # a > v > nbr => a > u > nbr
            face = mesh.face[fkey]
            a = mesh.face_vertex_ancestor(fkey, v)
            face[face.index(v)] = u

            if v in mesh.halfedge[a]:
                del mesh.halfedge[a][v]
            del mesh.halfedge[v][nbr]
            mesh.halfedge[a][u] = fkey
            mesh.halfedge[u][nbr] = fkey

        # only update what will not be updated in the previous part
        # verify what this is exactly
        # nbr > v > d => nbr > u > d
        if v in mesh.halfedge[nbr]:
            fkey = mesh.halfedge[nbr][v]
            del mesh.halfedge[nbr][v]
            mesh.halfedge[nbr][u] = fkey

    # delete V
    del mesh.halfedge[v]
    del mesh.vertex[v]


# split this up into more efficient cases
# - both not on boundary
# - u on boundary
# - v on boundary
# - u and v on boundary


def trimesh_collapse_edge(mesh, u, v, t=0.5, allow_boundary=False, fixed=None):
    """Collapse an edge to its first or second vertex, or to an intermediate
    point.

    Notes
    -----
    An edge can only be collapsed if the collapse is `legal`. A collapse is
    legal if it meets the following requirements:

        * any vertex `w` that is a neighbor of both `u` and `v` is a face
          of the mesh
        * `u` and `v` are not on the boundary
        * ...

    See [] for a detailed explanation of these requirements.

    Parameters
    ----------
    u : str
        The first vertex of the (half-) edge.
    v : str
        The second vertex of the (half-) edge.
    t : float
        Determines where to collapse to.
        If `t == 0.0` collapse to `u`.
        If `t == 1.0` collapse to `v`.
        If `0.0 < t < 1.0`, collapse to a point between `u` and `v`.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If `u` and `v` are not neighbors.

    Examples
    --------
    .. plot::
        :include-source:

        import compas

        from compas.datastructures import Mesh
        from compas.plotters import MeshPlotter

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        plotter = MeshPlotter(mesh)

        plotter.draw_vertices(text={key: key for key in mesh.vertices()}, radius=0.2)
        plotter.draw_faces(text={fkey: fkey for fkey in mesh.faces()})

        plotter.show()

    .. plot::
        :include-source:

        import compas

        from compas.datastructures import Mesh
        from compas.datastructures import mesh_quads_to_triangles
        from compas.datastructures import trimesh_collapse_edge
        from compas.plotters import MeshPlotter

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        mesh_quads_to_triangles(mesh)

        u, v = mesh.get_any_edge()

        trimesh_collapse_edge(mesh, u, v)

        plotter = MeshPlotter(mesh)

        plotter.draw_vertices(text={key: key for key in mesh.vertices()}, radius=0.2)
        plotter.draw_faces(text={fkey: fkey for fkey in mesh.faces()})

        plotter.show()

    """
    if t < 0.0:
        raise ValueError('Parameter t should be greater than or equal to 0.')
    if t > 1.0:
        raise ValueError('Parameter t should be smaller than or equal to 1.')

    # check collapse conditions
    if not is_collapse_legal(mesh, u, v, allow_boundary=allow_boundary):
        return False

    if mesh.is_vertex_on_boundary(u):
        t = 0.0

    # compare to fixed
    fixed = fixed or []
    if v in fixed or u in fixed:
        return False

    # move U
    x, y, z = mesh.edge_point(u, v, t)

    mesh.vertex[u]['x'] = x
    mesh.vertex[u]['y'] = y
    mesh.vertex[u]['z'] = z

    # UV face
    fkey = mesh.halfedge[u][v]

    if fkey is None:
        del mesh.halfedge[u][v]
    else:
        face = mesh.face[fkey]

        o = face[face.index(u) - 1]

        del mesh.halfedge[u][v]
        del mesh.halfedge[v][o]
        del mesh.halfedge[o][u]
        del mesh.face[fkey]

        if len(mesh.halfedge[o]) < 2:
            del mesh.halfedge[o]
            del mesh.vertex[o]
            del mesh.halfedge[u][o]

    # VU face
    fkey = mesh.halfedge[v][u]

    if fkey is None:
        del mesh.halfedge[v][u]
    else:
        face = mesh.face[fkey]

        o = face[face.index(v) - 1]

        del mesh.halfedge[v][u]
        del mesh.halfedge[u][o]
        del mesh.halfedge[o][v]
        del mesh.face[fkey]

        if len(mesh.halfedge[o]) < 2:
            del mesh.halfedge[o]
            del mesh.vertex[o]
            del mesh.halfedge[v][o]

    # neighborhood of V
    for nbr, fkey in list(mesh.halfedge[v].items()):

        if fkey is None:
            mesh.halfedge[u][nbr] = None
            del mesh.halfedge[v][nbr]
        else:
            # a > v > nbr => a > u > nbr
            face = mesh.face[fkey]
            a = face[face.index(v) - 1]
            mesh.face[fkey] = [a, u, nbr]

            if v in mesh.halfedge[a]:
                del mesh.halfedge[a][v]
            del mesh.halfedge[v][nbr]

            mesh.halfedge[a][u] = fkey
            mesh.halfedge[u][nbr] = fkey
            mesh.halfedge[nbr][a] = fkey

        # nbr > v > d => nbr > u > d
        if v in mesh.halfedge[nbr]:
            mesh.halfedge[nbr][u] = mesh.halfedge[nbr][v]
            del mesh.halfedge[nbr][v]

    # delete V
    del mesh.halfedge[v]
    del mesh.vertex[v]

    # clean up
    for nu in mesh.halfedge[u]:
        for nbr in mesh.halfedge[nu]:
            if nbr == v:
                mesh.halfedge[nu][u] = mesh.halfedge[nu][v]
                del mesh.halfedge[nu][v]

    return True


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures import Mesh
    from compas.datastructures import mesh_quads_to_triangles
    from compas.datastructures import trimesh_collapse_edge
    from compas.plotters import MeshPlotter

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    mesh_quads_to_triangles(mesh)

    trimesh_collapse_edge(mesh, 21, 27)
    trimesh_collapse_edge(mesh, 0, 6, allow_boundary=True)
    trimesh_collapse_edge(mesh, 1, 7, allow_boundary=True)

    plotter = MeshPlotter(mesh, figsize=(10, 7))

    plotter.draw_vertices(text={key: key for key in mesh.vertices()}, radius=0.2)
    plotter.draw_faces(text={fkey: fkey for fkey in mesh.faces()})

    plotter.show()
