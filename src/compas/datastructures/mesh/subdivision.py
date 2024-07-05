from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from copy import deepcopy
from math import cos
from math import pi

from compas.geometry import centroid_points
from compas.geometry import offset_polygon
from compas.itertools import iterable_like
from compas.itertools import pairwise


def subd_factory(cls):
    class SubdMesh(cls):
        _add_vertex = cls.add_vertex
        _add_face = cls.add_face
        _insert_vertex = cls.insert_vertex

        def add_vertex(self, x, y, z):
            key = self._max_vertex = self._max_vertex + 1
            if key not in self.vertex:
                self.vertex[key] = {}
                self.halfedge[key] = {}
            self.vertex[key] = dict(x=x, y=y, z=z)
            return key

        def add_face(self, vertices):
            fkey = self._max_face = self._max_face + 1
            self.face[fkey] = vertices
            self.facedata[fkey] = {}
            for i in range(-1, len(vertices) - 1):
                u = vertices[i]
                v = vertices[i + 1]
                self.halfedge[u][v] = fkey
                if u not in self.halfedge[v]:
                    self.halfedge[v][u] = None
            return fkey

        def insert_vertex(self, fkey):
            x, y, z = self.face_center(fkey)
            w = self.add_vertex(x=x, y=y, z=z)
            for u, v in self.face_halfedges(fkey):
                self.add_face([u, v, w])
            del self.face[fkey]
            return w

    return SubdMesh


def mesh_fast_copy(other):
    SubdMesh = subd_factory(type(other))
    subd = SubdMesh()
    subd.vertex = deepcopy(other.vertex)
    subd.face = deepcopy(other.face)
    subd.facedata = deepcopy(other.facedata)
    subd.halfedge = deepcopy(other.halfedge)
    subd._max_vertex = other._max_vertex
    subd._max_face = other._max_face
    return subd


# distinguish between subd of meshes with and without boundary
# closed vs. open
# pay attention to extraordinary points
# and to special rules on boundaries
# interpolation vs. approxmation?!
# add numerical versions to compas.datastructures.mesh.(algorithms.)numerical
# investigate meaning and definition of limit surface
# any subd algorithm should return a new subd mesh, leaving the control mesh intact


def mesh_subdivide(mesh, scheme="catmullclark", **options):
    """Subdivide the input mesh.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A mesh object.
    scheme : Literal['tri', 'quad', 'corner', 'catmullclark', 'doosabin', 'frames', 'loop'], optional
        The scheme according to which the mesh should be subdivided.
    **options : dict[str, Any], optional
        Optional additional keyword arguments.

    Returns
    -------
    :class:`compas.datastructures.Mesh`
        The subdivided mesh.

    Raises
    ------
    ValueError
        If the scheme is not supported.

    """
    if scheme == "tri":
        return mesh_subdivide_tri(mesh, **options)
    if scheme == "quad":
        return mesh_subdivide_quad(mesh, **options)
    if scheme == "corner":
        return mesh_subdivide_corner(mesh, **options)
    if scheme == "catmullclark":
        return mesh_subdivide_catmullclark(mesh, **options)
    if scheme == "doosabin":
        return mesh_subdivide_doosabin(mesh, **options)
    if scheme == "frames":
        return mesh_subdivide_frames(mesh, **options)
    if scheme == "loop":
        return trimesh_subdivide_loop(mesh, **options)

    raise ValueError("Scheme is not supported")


def mesh_subdivide_tri(mesh, k=1):
    """Subdivide a mesh using simple insertion of vertices.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        The mesh object that will be subdivided.
    k : int, optional
        The number of levels of subdivision.

    Returns
    -------
    :class:`compas.datastructures.Mesh`
        A new subdivided mesh.

    Examples
    --------
    >>> from compas.geometry import Box
    >>> from compas.datastructures import Mesh
    >>> box = Box.from_corner_corner_height([0.0, 0.0, 0.0], [1.0, 1.0, 0.0], 1.0)
    >>> mesh = Mesh.from_shape(box)
    >>> k = 2
    >>> subd = mesh_subdivide_tri(mesh, k=k)
    >>> mesh is subd
    False
    >>> type(mesh) is type(subd)
    True
    >>> k1 = sum(len(mesh.face_vertices(fkey)) for fkey in mesh.faces())
    >>> subd.number_of_faces() == (k1 if k == 1 else k1 * 3 ** (k - 1))
    True

    """
    cls = type(mesh)
    subd = mesh_fast_copy(mesh)
    for _ in range(k):
        for fkey in list(subd.faces()):
            subd.insert_vertex(fkey)
    return cls.__from_data__(subd.__data__)


def mesh_subdivide_quad(mesh, k=1):
    """Subdivide a mesh such that all faces are quads.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        The mesh object that will be subdivided.
    k : int, optional
        The number of levels of subdivision.

    Returns
    -------
    :class:`compas.datastructures.Mesh`
        A new subdivided mesh.

    Examples
    --------
    >>> from compas.geometry import Box
    >>> from compas.datastructures import Mesh
    >>> box = Box.from_corner_corner_height([0.0, 0.0, 0.0], [1.0, 1.0, 0.0], 1.0)
    >>> mesh = Mesh.from_shape(box)
    >>> k = 2
    >>> subd = mesh_subdivide_quad(mesh, k=k)
    >>> mesh is subd
    False
    >>> type(mesh) is type(subd)
    True
    >>> subd.number_of_faces() == mesh.number_of_faces() * 4**k
    True

    """
    cls = type(mesh)
    subd = mesh_fast_copy(mesh)
    for face in subd.faces():
        subd.facedata[face]["path"] = [face]
    for _ in range(k):
        faces = {face: subd.face_vertices(face)[:] for face in subd.faces()}
        face_centroid = {face: subd.face_centroid(face) for face in subd.faces()}
        for edge in list(subd.edges()):
            subd.split_edge(edge, allow_boundary=True)
        for face, vertices in faces.items():
            descendant = {i: j for i, j in subd.face_halfedges(face)}
            ancestor = {j: i for i, j in subd.face_halfedges(face)}
            x, y, z = face_centroid[face]
            c = subd.add_vertex(x=x, y=y, z=z)
            for i, vertex in enumerate(vertices):
                a = ancestor[vertex]
                d = descendant[vertex]
                newface = subd.add_face([a, vertex, d, c])
                subd.facedata[newface]["path"] = subd.facedata[face]["path"] + [i]
            del subd.face[face]
            del subd.facedata[face]
    subd2 = cls.__from_data__(subd.__data__)
    return subd2


def mesh_subdivide_corner(mesh, k=1):
    """Subdivide a mesh by cutting corners.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        The mesh object that will be subdivided.
    k : int, optional
        The number of levels of subdivision.

    Returns
    -------
    :class:`compas.datastructures.Mesh`
        A new subdivided mesh.

    Notes
    -----
    This is essentially the same as Loop subdivision, but applied to general meshes.

    """
    cls = type(mesh)
    for _ in range(k):
        subd = mesh_fast_copy(mesh)
        # split every edge
        for edge in list(subd.edges()):
            subd.split_edge(edge, allow_boundary=True)
        # create 4 new faces for every old face
        for fkey in mesh.faces():
            descendant = {i: j for i, j in subd.face_halfedges(fkey)}
            ancestor = {j: i for i, j in subd.face_halfedges(fkey)}
            center = []
            for key in mesh.face_vertices(fkey):
                a = ancestor[key]
                d = descendant[key]
                subd.add_face([a, key, d])
                center.append(a)
            subd.add_face(center)
            del subd.face[fkey]
        mesh = subd
    subd2 = cls.__from_data__(mesh.__data__)
    return subd2


def mesh_subdivide_catmullclark(mesh, k=1, fixed=None):
    """Subdivide a mesh using the Catmull-Clark algorithm.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        The mesh object that will be subdivided.
    k : int, optional
        The number of levels of subdivision.
    fixed : list[int], optional
        A list of fixed vertices.

    Returns
    -------
    :class:`compas.datastructures.Mesh`
        A new subdivided mesh.

    Notes
    -----
    Note that *Catmull-Clark* subdivision is like *Quad* subdivision, but with
    smoothing after every level of further subdivision. Smoothing is done
    according to the scheme prescribed by the Catmull-Clark algorithm.

    References
    ----------
    .. [1] Tony DeRose, Michael Kass and Tien Truong.
           Subdivision Surfaces in Character Animation.
           Pixar Animation Studios.
           see https://graphics.pixar.com/library/Geri/paper.pdf

    Examples
    --------
    >>> from compas.geometry import Box
    >>> from compas.datastructures import Mesh
    >>> box = Box.from_corner_corner_height([0.0, 0.0, 0.0], [1.0, 1.0, 0.0], 1.0)
    >>> mesh = Mesh.from_shape(box)
    >>> k = 2
    >>> subd = mesh_subdivide_catmullclark(mesh, k=k)
    >>> mesh is subd
    False
    >>> type(mesh) is type(subd)
    True
    >>> subd.number_of_faces() == mesh.number_of_faces() * 4**k
    True

    The algorithm supports "integer creasing" as described in
    Subdivision Surfaces in Character Animation [1]_.
    Creases are supported through the optional edge attribute "crease",
    which can be set to an integer value that defines how sharp the crease is wrt
    the number of subdivision steps.

    To add an infinitely sharp crease to an edge, set the "crease" attribute of the edge
    to a number higher than the number of subdivision steps.

    >>> from compas.geometry import Box, dot_vectors
    >>> from compas.datastructures import Mesh

    >>> cage = Mesh.from_shape(Box.from_width_height_depth(1, 1, 1))
    >>> cage.update_default_edge_attributes({"crease": 0})
    >>> top = sorted(cage.faces(), key=lambda face: dot_vectors(cage.face_normal(face), [0, 0, 1]))[-1]
    >>> cage.edges_attribute("crease", 5, keys=list(cage.face_halfedges(top)))

    >>> subd = cage.subdivided(k=4)

    """
    cls = type(mesh)

    if not fixed:
        fixed = []
    fixed = set(fixed)

    for _ in range(k):
        subd = mesh_fast_copy(mesh)

        # keep track of original connectivity and vertex locations

        # apply quad meshivision scheme
        # keep track of the created edge points that are not on the boundary
        # keep track track of the new edge points on the boundary
        # and their relation to the previous boundary points

        # quad subdivision
        # ======================================================================

        edgepoints = []

        for u, v in mesh.edges():
            w = subd.split_edge((u, v), allow_boundary=True)
            crease = mesh.edge_attribute((u, v), "crease") or 0

            if crease:
                edgepoints.append([w, True])
                subd.edge_attribute((u, w), "crease", crease - 1)
                subd.edge_attribute((w, v), "crease", crease - 1)
            else:
                edgepoints.append([w, False])

        fkey_xyz = {fkey: mesh.face_centroid(fkey) for fkey in mesh.faces()}

        for fkey in mesh.faces():
            descendant = {i: j for i, j in subd.face_halfedges(fkey)}
            ancestor = {j: i for i, j in subd.face_halfedges(fkey)}

            x, y, z = fkey_xyz[fkey]
            c = subd.add_vertex(x=x, y=y, z=z)

            for key in mesh.face_vertices(fkey):
                a = ancestor[key]
                d = descendant[key]

                subd.add_face([a, key, d, c])

            del subd.face[fkey]

        # update coordinates
        # ======================================================================

        # these are the coordinates before updating

        key_xyz = {key: subd.vertex_coordinates(key) for key in subd.vertex}

        # move each edge point to the average of the neighboring centroids and
        # the original end points

        for w, crease in edgepoints:
            if not crease:
                x, y, z = centroid_points([key_xyz[nbr] for nbr in subd.halfedge[w]])
                subd.vertex[w]["x"] = x
                subd.vertex[w]["y"] = y
                subd.vertex[w]["z"] = z

        # move each vertex to the weighted average of itself, the neighboring
        # centroids and the neighboring mipoints

        for key in mesh.vertices():
            if key in fixed:
                continue

            nbrs = mesh.vertex_neighbors(key)
            creases = mesh.edges_attribute("crease", keys=[(key, nbr) for nbr in nbrs])

            C = sum(1 if crease else 0 for crease in creases)

            if C < 2:
                fnbrs = [mesh.face_centroid(fkey) for fkey in mesh.vertex_faces(key) if fkey is not None]
                enbrs = [key_xyz[nbr] for nbr in subd.halfedge[key]]  # this should be the location of the original neighbour
                n = len(enbrs)
                v = n - 3.0
                F = centroid_points(fnbrs)
                E = centroid_points(enbrs)
                V = key_xyz[key]
                x = (F[0] + 2.0 * E[0] + v * V[0]) / n
                y = (F[1] + 2.0 * E[1] + v * V[1]) / n
                z = (F[2] + 2.0 * E[2] + v * V[2]) / n
                subd.vertex[key]["x"] = x
                subd.vertex[key]["y"] = y
                subd.vertex[key]["z"] = z

            elif C == 2:
                V = key_xyz[key]
                E = [0, 0, 0]
                for nbr, crease in zip(nbrs, creases):
                    if crease:
                        x, y, z = key_xyz[nbr]
                        E[0] += x
                        E[1] += y
                        E[2] += z
                x = (6 * V[0] + E[0]) / 8
                y = (6 * V[1] + E[1]) / 8
                z = (6 * V[2] + E[2]) / 8
                subd.vertex[key]["x"] = x
                subd.vertex[key]["y"] = y
                subd.vertex[key]["z"] = z
            else:
                pass

        mesh = subd

    subd2 = cls.__from_data__(mesh.__data__)
    return subd2


def mesh_subdivide_doosabin(mesh, k=1, fixed=None):
    """Subdivide a mesh following the doo-sabin scheme.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        The mesh object that will be subdivided.
    k : int, optional
        The number of levels of subdivision.
    fixed : list[int], optional
        A list of fixed vertices.

    Returns
    -------
    :class:`compas.datastructures.Mesh`
        A new subdivided mesh.

    Examples
    --------
    >>> from compas.geometry import Box
    >>> from compas.datastructures import Mesh
    >>> box = Box.from_corner_corner_height([0.0, 0.0, 0.0], [1.0, 1.0, 0.0], 1.0)
    >>> mesh = Mesh.from_shape(box)
    >>> k = 2
    >>> subd = mesh_subdivide_doosabin(mesh, k=k)
    >>> mesh is subd
    False
    >>> type(mesh) is type(subd)
    True

    """
    if not fixed:
        fixed = []

    fixed = set(fixed)

    cls = type(mesh)
    SubdMesh = subd_factory(cls)

    for _ in range(k):
        old_xyz = {key: mesh.vertex_coordinates(key) for key in mesh.vertices()}
        fkey_old_new = {fkey: {} for fkey in mesh.faces()}

        subd = SubdMesh()

        for fkey in mesh.faces():
            vertices = mesh.face_vertices(fkey)
            n = len(vertices)

            face = []

            for i in range(n):
                old = vertices[i]

                cx, cy, cz = 0, 0, 0

                for j in range(n):
                    x, y, z = old_xyz[vertices[j]]

                    if i == j:
                        alpha = (n + 5.0) / (4.0 * n)
                    else:
                        alpha = (3.0 + 2.0 * cos(2.0 * pi * (i - j) / n)) / (4.0 * n)

                    cx += alpha * x
                    cy += alpha * y
                    cz += alpha * z

                new = subd.add_vertex(cx, cy, cz)
                fkey_old_new[fkey][old] = new

                face.append(new)

            subd.add_face(face)

        boundary = set(mesh.vertices_on_boundary())

        for key in mesh.vertices():
            if key in boundary:
                continue

            face = [fkey_old_new[fkey][key] for fkey in mesh.vertex_faces(key, ordered=True) if fkey is not None]

            subd.add_face(face[::-1])

        edges = set()

        for u in mesh.halfedge:
            for v in mesh.halfedge[u]:
                if (u, v) in edges:
                    continue

                edges.add((u, v))
                edges.add((v, u))

                uv_fkey = mesh.halfedge[u][v]
                vu_fkey = mesh.halfedge[v][u]

                if uv_fkey is None or vu_fkey is None:
                    continue

                face = [
                    fkey_old_new[uv_fkey][u],
                    fkey_old_new[vu_fkey][u],
                    fkey_old_new[vu_fkey][v],
                    fkey_old_new[uv_fkey][v],
                ]
                subd.add_face(face)

        mesh = subd

    subd2 = cls.__from_data__(mesh.__data__)
    return subd2


def mesh_subdivide_frames(mesh, offset, add_windows=False):
    """Subdivide a mesh by creating offset frames and windows on its faces.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        The mesh object to be subdivided.
    offset : float | dict[int, float]
        The offset distance to create the frames.
        A single value will result in a constant offset everywhere.
        A dictionary mapping faces to offset values will be processed accordingly.
    add_windows : bool, optional
        If True, add a window face in the frame opening.

    Returns
    -------
    :class:`compas.datastructures.Mesh`
        A new subdivided mesh.

    """
    cls = type(mesh)
    SubdMesh = subd_factory(cls)

    subd = SubdMesh()

    # 0. pre-compute offset distances
    if not isinstance(offset, dict):
        distances = iterable_like(mesh.faces(), [offset], offset)
        offset = {fkey: od for fkey, od in zip(mesh.faces(), distances)}

    # 1. add vertices
    newkeys = {}
    for vkey, attr in mesh.vertices(True):
        newkeys[vkey] = subd.add_vertex(*mesh.vertex_coordinates(vkey))

    # 2. add faces
    for fkey in mesh.faces():
        face = [newkeys[vkey] for vkey in mesh.face_vertices(fkey)]
        d = offset.get(fkey)

        # 2a. add face and break if no offset is found
        if d is None:
            subd.add_face(face)
            continue

        polygon = offset_polygon(mesh.face_coordinates(fkey), d)

        # 2a. add offset vertices
        window = []
        for xyz in polygon:
            x, y, z = xyz
            new_vkey = subd.add_vertex(x=x, y=y, z=z)
            window.append(new_vkey)

        # 2b. frame faces
        face = face + face[:1]
        window = window + window[:1]
        for sa, sb in zip(pairwise(face), pairwise(window)):
            subd.add_face([sa[0], sa[1], sb[1], sb[0]])

        # 2c. window face
        if add_windows:
            subd.add_face(window)

    return cls.__from_data__(subd.__data__)


def trimesh_subdivide_loop(mesh, k=1, fixed=None):
    """Subdivide a triangle mesh using the Loop algorithm.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        The mesh object that will be subdivided.
    k : int, optional
        The number of levels of subdivision.
    fixed : list[int], optional
        A list of fixed vertices.

    Returns
    -------
    :class:`compas.datastructures.Mesh`
        A new subdivided mesh.

    Examples
    --------
    Make a low poly mesh from a box shape.
    Triangulate the faces.

    >>> from compas.geometry import Box
    >>> from compas.datastructures import Mesh
    >>> box = Box.from_corner_corner_height([0.0, 0.0, 0.0], [1.0, 1.0, 0.0], 1.0)
    >>> mesh = Mesh.from_shape(box)
    >>> mesh.quads_to_triangles()

    Subdivide 2 times.

    >>> k = 2
    >>> subd = trimesh_subdivide_loop(mesh, k=k)

    Compare low-poly cage with subdivision mesh.

    >>> mesh is subd
    False
    >>> type(mesh) is type(subd)
    True
    >>> subd.number_of_faces() == mesh.number_of_faces() * (3 + 1) ** k
    True

    """
    cls = type(mesh)

    if not fixed:
        fixed = []

    fixed = set(fixed)

    subd = mesh_fast_copy(mesh)

    for _ in range(k):
        key_xyz = {key: subd.vertex_coordinates(key) for key in subd.vertices()}
        fkey_vertices = {fkey: subd.face_vertices(fkey)[:] for fkey in subd.faces()}
        uv_w = {(u, v): subd.face_vertex_ancestor(fkey, u) for fkey in subd.faces() for u, v in subd.face_halfedges(fkey)}
        boundary = set(subd.vertices_on_boundary())

        for key in subd.vertices():
            nbrs = subd.vertex_neighbors(key)

            if key in boundary:
                xyz = key_xyz[key]

                x = 0.75 * xyz[0]
                y = 0.75 * xyz[1]
                z = 0.75 * xyz[2]

                for n in nbrs:
                    if subd.halfedge[key][n] is None or subd.halfedge[n][key] is None:
                        xyz = key_xyz[n]

                        x += 0.125 * xyz[0]
                        y += 0.125 * xyz[1]
                        z += 0.125 * xyz[2]

            else:
                n = len(nbrs)

                if n == 3:
                    a = 3.0 / 16.0
                else:
                    a = 3.0 / (8 * n)

                xyz = key_xyz[key]

                nbrs = [key_xyz[nbr] for nbr in nbrs]
                nbrs = [sum(axis) for axis in zip(*nbrs)]

                x = (1.0 - n * a) * xyz[0] + a * nbrs[0]
                y = (1.0 - n * a) * xyz[1] + a * nbrs[1]
                z = (1.0 - n * a) * xyz[2] + a * nbrs[2]

            subd.vertex[key]["x"] = x
            subd.vertex[key]["y"] = y
            subd.vertex[key]["z"] = z

        edgepoints = {}

        # odd vertices
        for u, v in list(subd.edges()):
            w = subd.split_edge((u, v), allow_boundary=True)

            edgepoints[(u, v)] = w
            edgepoints[(v, u)] = w

            a = key_xyz[u]
            b = key_xyz[v]

            if (u, v) in uv_w and (v, u) in uv_w:
                c = key_xyz[uv_w[(u, v)]]
                d = key_xyz[uv_w[(v, u)]]
                xyz = [(3.0 / 8.0) * (a[i] + b[i]) + (1.0 / 8.0) * (c[i] + d[i]) for i in range(3)]

            else:
                xyz = [0.5 * (a[i] + b[i]) for i in range(3)]

            subd.vertex[w]["x"] = xyz[0]
            subd.vertex[w]["y"] = xyz[1]
            subd.vertex[w]["z"] = xyz[2]

        # new faces
        for fkey, vertices in fkey_vertices.items():
            u, v, w = vertices

            uv = edgepoints[(u, v)]
            vw = edgepoints[(v, w)]
            wu = edgepoints[(w, u)]

            subd.add_face([wu, u, uv])
            subd.add_face([uv, v, vw])
            subd.add_face([vw, w, wu])
            subd.add_face([uv, vw, wu])

            del subd.face[fkey]

    return cls.__from_data__(subd.__data__)
