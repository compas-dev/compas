from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import cos
from math import pi
from copy import deepcopy

from compas.geometry import centroid_points
from compas.geometry import offset_polygon

from compas.utilities import iterable_like
from compas.utilities import pairwise

from .core import BaseMesh


__all__ = [
    'mesh_subdivide',
    'mesh_subdivide_tri',
    'mesh_subdivide_corner',
    'mesh_subdivide_quad',
    'mesh_subdivide_catmullclark',
    'mesh_subdivide_doosabin',
    'mesh_subdivide_frames',
    'trimesh_subdivide_loop',
]


def mesh_fast_copy(other):
    subd = SubdMesh()
    subd.vertex = deepcopy(other.vertex)
    subd.face = deepcopy(other.face)
    # subd.edgedata = deepcopy(other.edgedata)
    subd.facedata = deepcopy(other.facedata)
    subd.halfedge = deepcopy(other.halfedge)
    subd._max_vertex = other._max_vertex
    subd._max_face = other._max_face
    return subd


class SubdMesh(BaseMesh):

    from .core import mesh_split_edge

    _add_vertex = BaseMesh.add_vertex
    _add_face = BaseMesh.add_face
    _insert_vertex = BaseMesh.insert_vertex

    split_edge = mesh_split_edge

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

# distinguish between subd of meshes with and without boundary
# closed vs. open
# pay attention to extraordinary points
# and to special rules on boundaries
# interpolation vs. approxmation?!
# add numerical versions to compas.datastructures.mesh.(algorithms.)numerical
# investigate meaning and definition of limit surface
# any subd algorithm should return a new subd mesh, leaving the control mesh intact


def mesh_subdivide(mesh, scheme='catmullclark', **options):
    """Subdivide the input mesh.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.
    scheme : {'tri', 'corner', 'catmullclark', 'doosabin'}, optional
        The scheme according to which the mesh should be subdivided.
        Default is ``'catmullclark'``.
    options : dict
        Optional additional keyword arguments.

    Returns
    -------
    Mesh
        The subdivided mesh.

    Raises
    ------
    NotImplementedError
        If the scheme is not supported.

    """
    if scheme == 'tri':
        return mesh_subdivide_tri(mesh, **options)
    if scheme == 'quad':
        return mesh_subdivide_quad(mesh, **options)
    if scheme == 'corner':
        return mesh_subdivide_corner(mesh, **options)
    if scheme == 'catmullclark':
        return mesh_subdivide_catmullclark(mesh, **options)
    if scheme == 'doosabin':
        return mesh_subdivide_doosabin(mesh, **options)

    raise NotImplementedError


def mesh_subdivide_tri(mesh, k=1):
    """Subdivide a mesh using simple insertion of vertices.

    Parameters
    ----------
    mesh : Mesh
        The mesh object that will be subdivided.
    k : int
        Optional. The number of levels of subdivision. Default is ``1``.

    Returns
    -------
    Mesh
        A new subdivided mesh.

    Examples
    --------
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
    return cls.from_data(subd.data)


def mesh_subdivide_quad(mesh, k=1):
    """Subdivide a mesh such that all faces are quads.

    Parameters
    ----------
    mesh : Mesh
        The mesh object that will be subdivided.
    k : int
        Optional. The number of levels of subdivision. Default is ``1``.

    Returns
    -------
    Mesh
        A new subdivided mesh.

    Examples
    --------
    >>> box = Box.from_corner_corner_height([0.0, 0.0, 0.0], [1.0, 1.0, 0.0], 1.0)
    >>> mesh = Mesh.from_shape(box)
    >>> k = 2
    >>> subd = mesh_subdivide_quad(mesh, k=k)
    >>> mesh is subd
    False
    >>> type(mesh) is type(subd)
    True
    >>> subd.number_of_faces() == mesh.number_of_faces() * 4 ** k
    True

    """
    cls = type(mesh)
    subd = mesh_fast_copy(mesh)
    for face in subd.faces():
        subd.facedata[face]['path'] = [face]
    for _ in range(k):
        faces = {face: subd.face_vertices(face)[:] for face in subd.faces()}
        face_centroid = {face: subd.face_centroid(face) for face in subd.faces()}
        for u, v in list(subd.edges()):
            subd.split_edge(u, v, allow_boundary=True)
        for face, vertices in faces.items():
            descendant = {i: j for i, j in subd.face_halfedges(face)}
            ancestor = {j: i for i, j in subd.face_halfedges(face)}
            x, y, z = face_centroid[face]
            c = subd.add_vertex(x=x, y=y, z=z)
            for i, vertex in enumerate(vertices):
                a = ancestor[vertex]
                d = descendant[vertex]
                newface = subd.add_face([a, vertex, d, c])
                subd.facedata[newface]['path'] = subd.facedata[face]['path'] + [i]
            del subd.face[face]
            del subd.facedata[face]
    subd2 = cls.from_data(subd.data)
    return subd2


def mesh_subdivide_corner(mesh, k=1):
    """Subdivide a mesh by cutting corners.

    Parameters
    ----------
    mesh : Mesh
        The mesh object that will be subdivided.
    k : int
        Optional. The number of levels of subdivision. Default is ``1``.

    Returns
    -------
    Mesh
        A new subdivided mesh.

    Notes
    -----
    This is essentially the same as Loop subdivision, but applied to general
    meshes.

    """
    cls = type(mesh)
    for _ in range(k):
        subd = mesh_fast_copy(mesh)
        # split every edge
        for u, v in list(subd.edges()):
            subd.split_edge(u, v, allow_boundary=True)
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
    subd2 = cls.from_data(mesh.data)
    return subd2


def mesh_subdivide_catmullclark(mesh, k=1, fixed=None):
    """Subdivide a mesh using the Catmull-Clark algorithm.

    Parameters
    ----------
    mesh : Mesh
        The mesh object that will be subdivided.
    k : int
        Optional. The number of levels of subdivision. Default is ``1``.
    fixed : list
        Optional. A list of fixed vertices. Default is ``None``.

    Returns
    -------
    Mesh
        A new subdivided mesh.

    Notes
    -----
    Note that *Catmull-Clark* subdivision is like *Quad* subdivision, but with
    smoothing after every level of further subdivision. Smoothing is done
    according to the scheme prescribed by the Catmull-Clark algorithm.

    Examples
    --------
    >>> box = Box.from_corner_corner_height([0.0, 0.0, 0.0], [1.0, 1.0, 0.0], 1.0)
    >>> mesh = Mesh.from_shape(box)
    >>> k = 2
    >>> subd = mesh_subdivide_catmullclark(mesh, k=k)
    >>> mesh is subd
    False
    >>> type(mesh) is type(subd)
    True
    >>> subd.number_of_faces() == mesh.number_of_faces() * 4 ** k
    True

    """
    cls = type(mesh)
    if not fixed:
        fixed = []
    fixed = set(fixed)

    for _ in range(k):
        subd = mesh_fast_copy(mesh)

        # keep track of original connectivity and vertex locations

        bkeys = set(subd.vertices_on_boundary())
        bkey_edgepoints = {key: [] for key in bkeys}

        # apply quad meshivision scheme
        # keep track of the created edge points that are not on the boundary
        # keep track track of the new edge points on the boundary
        # and their relation to the previous boundary points

        # quad subdivision
        # ======================================================================

        edgepoints = []

        for u, v in mesh.edges():

            w = subd.split_edge(u, v, allow_boundary=True)

            # document why this is necessary
            # everything else in this loop is just quad subdivision
            if u in bkeys and v in bkeys:

                bkey_edgepoints[u].append(w)
                bkey_edgepoints[v].append(w)

                continue

            edgepoints.append(w)

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

        for w in edgepoints:
            x, y, z = centroid_points([key_xyz[nbr] for nbr in subd.halfedge[w]])

            subd.vertex[w]['x'] = x
            subd.vertex[w]['y'] = y
            subd.vertex[w]['z'] = z

        # move each vertex to the weighted average of itself, the neighboring
        # centroids and the neighboring mipoints

        for key in mesh.vertices():
            if key in fixed:
                continue

            if key in bkeys:
                nbrs = set(bkey_edgepoints[key])
                nbrs = [key_xyz[nbr] for nbr in nbrs]
                e = 0.5
                v = 0.5
                E = [coord * e for coord in centroid_points(nbrs)]
                V = [coord * v for coord in key_xyz[key]]
                x, y, z = [E[_] + V[_] for _ in range(3)]

            else:
                fnbrs = [mesh.face_centroid(fkey) for fkey in mesh.vertex_faces(key) if fkey is not None]
                nbrs = [key_xyz[nbr] for nbr in subd.halfedge[key]]
                n = float(len(nbrs))
                f = 1.0 / n
                e = 2.0 / n
                v = (n - 3.0) / n
                F = centroid_points(fnbrs)
                E = centroid_points(nbrs)
                V = key_xyz[key]
                x = f * F[0] + e * E[0] + v * V[0]
                y = f * F[1] + e * E[1] + v * V[1]
                z = f * F[2] + e * E[2] + v * V[2]

            subd.vertex[key]['x'] = x
            subd.vertex[key]['y'] = y
            subd.vertex[key]['z'] = z

        mesh = subd

    subd2 = cls.from_data(mesh.data)
    return subd2


def mesh_subdivide_doosabin(mesh, k=1, fixed=None):
    """Subdivide a mesh following the doo-sabin scheme.

    Parameters
    ----------
    mesh : Mesh
        The mesh object that will be subdivided.
    k : int
        Optional. The number of levels of subdivision. Default is ``1``.
    fixed : list
        Optional. A list of fixed vertices. Default is ``None``.

    Returns
    -------
    Mesh
        A new subdivided mesh.

    Examples
    --------
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
                        alpha = (n + 5.) / (4. * n)
                    else:
                        alpha = (3. + 2. * cos(2. * pi * (i - j) / n)) / (4. * n)

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
                    fkey_old_new[uv_fkey][v]
                ]
                subd.add_face(face)

        mesh = subd

    subd2 = cls.from_data(mesh.data)
    return subd2


def mesh_subdivide_frames(mesh, offset, add_windows=False):
    """Subdivide a mesh by creating offset frames and windows on its faces.

    Parameters
    ----------
    mesh : Mesh
        The mesh object to be subdivided.
    offset : float or dict
        The offset distance to create the frames.
        A single value will result in a constant offset everywhere.
        A dictionary mapping facekey: offset will be processed accordingly.
    add_windows : boolean
        Optional. Flag to add window face. Default is ``False``.

    Returns
    -------
    Mesh
        A new subdivided mesh.

    Examples
    --------
    >>>

    """

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

    return subd


def trimesh_subdivide_loop(mesh, k=1, fixed=None):
    """Subdivide a triangle mesh using the Loop algorithm.

    Parameters
    ----------
    mesh : Mesh
        The mesh object that will be subdivided.
    k : int
        Optional. The number of levels of subdivision. Default is ``1``.
    fixed : list
        Optional. A list of fixed vertices. Default is ``None``.

    Returns
    -------
    Mesh
        A new subdivided mesh.

    Examples
    --------
    Make a low poly mesh from a box shape.
    Triangulate the faces.
    >>> box = Box.from_corner_corner_height([0.0, 0.0, 0.0], [1.0, 1.0, 0.0], 1.0)
    >>> mesh = Mesh.from_shape(box)
    >>> mesh_quads_to_triangles(mesh)

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
                    a = 3. / 16.
                else:
                    a = 3. / (8 * n)

                xyz = key_xyz[key]

                nbrs = [key_xyz[nbr] for nbr in nbrs]
                nbrs = [sum(axis) for axis in zip(*nbrs)]

                x = (1. - n * a) * xyz[0] + a * nbrs[0]
                y = (1. - n * a) * xyz[1] + a * nbrs[1]
                z = (1. - n * a) * xyz[2] + a * nbrs[2]

            subd.vertex[key]['x'] = x
            subd.vertex[key]['y'] = y
            subd.vertex[key]['z'] = z

        edgepoints = {}

        # odd vertices
        for u, v in list(subd.edges()):

            w = subd.split_edge(u, v, allow_boundary=True)

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

            subd.vertex[w]['x'] = xyz[0]
            subd.vertex[w]['y'] = xyz[1]
            subd.vertex[w]['z'] = xyz[2]

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

    subd2 = cls.from_data(subd.data)
    return subd2


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest
    import compas  # noqa: F401
    from compas.datastructures import mesh_quads_to_triangles  # noqa: F401
    from compas.datastructures import Mesh  # noqa: F401
    from compas.geometry import Box  # noqa: F401
    doctest.testmod(globs=globals())

    # from compas.datastructures import Mesh
    # from compas.geometry import Box
    # from compas.utilities import print_profile
    # from compas_viewers.multimeshviewer import MultiMeshViewer

    # subdivide = print_profile(mesh_subdivide_quad)

    # box = Box.from_width_height_depth(10.0, 10.0, 10.0)
    # mesh = Mesh.from_shape(box)
    # mesh.default_face_attributes.update(path=[])
    # subd = subdivide(mesh, k=3)

    # print(subd.face_attribute(subd.get_any_face(), 'path'))

    # # print(mesh.number_of_faces())

    # viewer = MultiMeshViewer()
    # viewer.meshes = [subd]
    # viewer.show()
