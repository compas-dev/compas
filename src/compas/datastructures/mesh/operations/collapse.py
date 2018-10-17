from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = [
    'mesh_collapse_edge',
    'trimesh_collapse_edge',
]


def is_collapse_legal(mesh, u, v, allow_boundary=False):
    """Verify if the requested collapse is legal fro a triangle mesh.

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
    # collapsing of boundary vertices is currently not supported
    # change this to `and` to support collapsing to or from the boundary
    if not allow_boundary:
        if mesh.is_vertex_on_boundary(v) or mesh.is_vertex_on_boundary(u):
            return False

    # check for contained faces
    for nbr in mesh.halfedge[u]:
        if nbr in mesh.halfedge[v]:
            # check if U > V > NBR is a face
            fkey = mesh.halfedge[u][v]
            if fkey != mesh.halfedge[v][nbr] or fkey != mesh.halfedge[nbr][u]:
                # check if V > U > NBR is a face
                fkey = mesh.halfedge[v][u]
                if fkey != mesh.halfedge[u][nbr] or fkey != mesh.halfedge[nbr][v]:
                    return False

    for nbr in mesh.halfedge[v]:
        if nbr in mesh.halfedge[u]:
            # check if U > V > NBR is a face
            fkey = mesh.halfedge[u][v]
            if fkey != mesh.halfedge[v][nbr] or fkey != mesh.halfedge[nbr][u]:
                # check if V > U > NBR is a face
                fkey = mesh.halfedge[v][u]
                if fkey != mesh.halfedge[u][nbr] or fkey != mesh.halfedge[nbr][v]:
                    return False

    return True


def mesh_collapse_edge(self, u, v, t=0.5, allow_boundary=False, fixed=None):
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

    # # collapsing of boundary vertices is currently not supported
    # # change this to `and` to support collapsing to or from the boundary
    # if self.is_vertex_on_boundary(u) or self.is_vertex_on_boundary(v):
    #     return

    # # check for contained faces
    # for nbr in self.halfedge[u]:
    #     if nbr in self.halfedge[v]:
    #         # check if U > V > NBR is a face
    #         if (self.halfedge[u][v] != self.halfedge[v][nbr] or self.halfedge[u][v] != self.halfedge[nbr][u]):
    #             # check if V > U > NBR is a face
    #             if (self.halfedge[v][u] != self.halfedge[u][nbr] or self.halfedge[v][u] != self.halfedge[nbr][v]):
    #                 return
    # for nbr in self.halfedge[v]:
    #     if nbr in self.halfedge[u]:
    #         # check if U > V > NBR is a face
    #         if (self.halfedge[u][v] != self.halfedge[v][nbr] or self.halfedge[u][v] != self.halfedge[nbr][u]):
    #             # check if V > U > NBR is a face
    #             if (self.halfedge[v][u] != self.halfedge[u][nbr] or self.halfedge[v][u] != self.halfedge[nbr][v]):
    #                 return

    # check collapse conditions
    if not is_collapse_legal(self, u, v, allow_boundary=allow_boundary):
        return False

    # compare to fixed
    fixed = fixed or []
    if v in fixed or u in fixed:
        return False

    # move U
    x, y, z = self.edge_point(u, v, t)
    self.vertex[u]['x'] = x
    self.vertex[u]['y'] = y
    self.vertex[u]['z'] = z

    # UV face
    fkey = self.halfedge[u][v]

    if fkey is None:
        del self.halfedge[u][v]

    else:
        face = self.face_vertices(fkey)
        f = len(face)

        # switch between UV face sizes
        # note: in a triself this is not necessary!
        if f < 3:
            raise Exception("Invalid self face: {}".format(fkey))
        if f == 3:
            # delete UV
            o = face[face.index(u) - 1]
            del self.halfedge[u][v]
            del self.halfedge[v][o]
            del self.halfedge[o][u]
            del self.face[fkey]
        else:
            # u > v > d => u > d
            d = self.face_vertex_descendant(fkey, v)
            face.remove(v)
            del self.halfedge[u][v]
            del self.halfedge[v][d]
            self.halfedge[u][d] = fkey

    # VU face
    fkey = self.halfedge[v][u]

    if fkey is None:
        del self.halfedge[v][u]

    else:
        face = self.face_vertices(fkey)
        f = len(face)

        # switch between VU face sizes
        # note: in a triself this is not necessary!
        if f < 3:
            raise Exception("Invalid mesh face: {}".format(fkey))
        if f == 3:
            # delete UV
            o = face[face.index(v) - 1]
            del self.halfedge[v][u]  # the collapsing halfedge
            del self.halfedge[u][o]
            del self.halfedge[o][v]
            del self.face[fkey]
        else:
            # a > v > u => a > u
            a = self.face_vertex_ancestor(fkey, v)
            face.remove(v)
            del self.halfedge[a][v]
            del self.halfedge[v][u]
            self.halfedge[a][u] = fkey

    # V neighbors and halfedges coming into V
    for nbr, fkey in list(self.halfedge[v].items()):

        if fkey is None:
            self.halfedge[u][nbr] = None
            del self.halfedge[v][nbr]
        else:
            # a > v > nbr => a > u > nbr
            face = self.face[fkey]
            a = self.face_vertex_ancestor(fkey, v)
            face[face.index(v)] = u

            if v in self.halfedge[a]:
                del self.halfedge[a][v]
            del self.halfedge[v][nbr]
            self.halfedge[a][u] = fkey
            self.halfedge[u][nbr] = fkey

        # only update what will not be updated in the previous part
        # verify what this is exactly
        # nbr > v > d => nbr > u > d
        if v in self.halfedge[nbr]:
            fkey = self.halfedge[nbr][v]
            del self.halfedge[nbr][v]
            self.halfedge[nbr][u] = fkey

    # delete V
    del self.halfedge[v]
    del self.vertex[v]


# split this up into more efficient cases
# - both not on boundary
# - u on boundary
# - v on boundary
# - u and v on boundary


def trimesh_collapse_edge(self, u, v, t=0.5, allow_boundary=False, fixed=None):
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
        from compas.plotters import MeshPlotter
        from compas.topology import mesh_quads_to_triangles

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        mesh_quads_to_triangles(mesh)

        u, v = mesh.get_any_edge()

        mesh.collapse_edge_tri(u, v)

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
    if not is_collapse_legal(self, u, v, allow_boundary=allow_boundary):
        return False

    # compare to fixed
    fixed = fixed or []
    if v in fixed or u in fixed:
        return False

    # move U
    x, y, z = self.edge_point(u, v, t)

    self.vertex[u]['x'] = x
    self.vertex[u]['y'] = y
    self.vertex[u]['z'] = z

    # UV face
    fkey = self.halfedge[u][v]

    if fkey is None:
        del self.halfedge[u][v]
    else:
        face = self.face[fkey]

        o = face[face.index(u) - 1]

        del self.halfedge[u][v]
        del self.halfedge[v][o]
        del self.halfedge[o][u]
        del self.face[fkey]

        if len(self.halfedge[o]) < 2:
            del self.halfedge[o]
            del self.vertex[o]
            del self.halfedge[u][o]

    # VU face
    fkey = self.halfedge[v][u]

    if fkey is None:
        del self.halfedge[v][u]
    else:
        face = self.face[fkey]

        o = face[face.index(v) - 1]

        del self.halfedge[v][u]
        del self.halfedge[u][o]
        del self.halfedge[o][v]
        del self.face[fkey]

        if len(self.halfedge[o]) < 2:
            del self.halfedge[o]
            del self.vertex[o]
            del self.halfedge[v][o]

    # neighborhood of V
    for nbr, fkey in list(self.halfedge[v].items()):

        if fkey is None:
            self.halfedge[u][nbr] = None
            del self.halfedge[v][nbr]
        else:
            # a > v > nbr => a > u > nbr
            face = self.face[fkey]
            a = face[face.index(v) - 1]
            self.face[fkey] = [a, u, nbr]

            if v in self.halfedge[a]:
                del self.halfedge[a][v]
            del self.halfedge[v][nbr]

            self.halfedge[a][u] = fkey
            self.halfedge[u][nbr] = fkey
            self.halfedge[nbr][a] = fkey

        # nbr > v > d => nbr > u > d
        if v in self.halfedge[nbr]:
            self.halfedge[nbr][u] = self.halfedge[nbr][v]
            del self.halfedge[nbr][v]

    # delete V
    del self.halfedge[v]
    del self.vertex[v]

    # clean up
    for nu in self.halfedge[u]:
        for nbr in self.halfedge[nu]:
            if nbr == v:
                self.halfedge[nu][u] = self.halfedge[nu][v]
                del self.halfedge[nu][v]

    return True


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures import Mesh
    from compas.plotters import MeshPlotter
    from compas.topology import mesh_quads_to_triangles

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    mesh_quads_to_triangles(mesh)

    mesh.swap_edge_tri(14, 19)
    mesh.swap_edge_tri(21, 16)

    mesh.collapse_edge_tri(21, 15)

    plotter = MeshPlotter(mesh, figsize=(10, 7))

    plotter.draw_vertices(text={key: key for key in mesh.vertices()}, radius=0.2)
    plotter.draw_faces(text={fkey: fkey for fkey in mesh.faces()})

    plotter.show()
