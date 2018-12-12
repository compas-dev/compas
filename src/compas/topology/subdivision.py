"""
Subdivision surfaces
====================

.. note::

    This is a combination of the following online resources:

    * https://en.wikipedia.org/wiki/Subdivision_surface
    * 

A subdivision surface is a method of representing a smooth surface via the
specification of a coarser piecewise linear polygon mesh.

The smooth surface can be calculated from the coarse mesh as the limit of recursive
subdivision of each polygonal face into smaller faces that better approximate the 
smooth surface.


"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import cos
from math import pi

from compas.datastructures import Mesh

from compas.geometry import centroid_points


__all__ = [
    'mesh_subdivide',
    'mesh_subdivide_tri',
    'mesh_subdivide_corner',
    'mesh_subdivide_quad',
    'mesh_subdivide_catmullclark',
    'mesh_subdivide_doosabin',
    'trimesh_subdivide_loop',
]


class SubdMesh(Mesh):

    # def vertex_coordinates(self, key):
    #     return self.vertex[key]

    def add_vertex(self, x, y, z):
        key = self._max_int_key = self._max_int_key + 1

        if key not in self.vertex:
            self.vertex[key] = {}
            self.halfedge[key] = {}

        self.vertex[key] = dict(x=x, y=y, z=z)

        return key

    def add_face(self, vertices):
        fkey = self._max_int_fkey = self._max_int_fkey + 1

        self.face[fkey] = vertices
        self.facedata[fkey] = {}

        for u, v in self._cycle_keys(vertices):
            self.halfedge[u][v] = fkey
            if u not in self.halfedge[v]:
                self.halfedge[v][u] = None

        return fkey


# distinguish between subd of meshes with and without boundary
# closed vs. open
# pay attention to extraordinary points
# and to special rules on boundaries
# interpolation vs. approxmation?!
# add numerical versions to compas.datastructures.mesh.(algorithms.)numerical
# investigate meaning and definition of limit surface
# any subd algorithm should return a new subd mesh, leaving the control mesh intact


def mesh_subdivide(mesh, scheme='tri', **options):
    """Subdivide the input mesh.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.
    scheme : {'tri', 'corner', 'catmullclark', 'doosabin'}.
        The scheme according to which the mesh should be subdivided.
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

    """

    for _ in range(k):
        subd = mesh.copy()

        for fkey in mesh.faces():
            subd.insert_vertex(fkey)

        mesh = subd

    return mesh


def mesh_subdivide_quad(mesh, k=1):
    """Subdivide a mesh such that all faces are quads.
    """

    for _ in range(k):
        subd = mesh.copy()

        for u, v in list(subd.edges()):
            subd.split_edge(u, v, allow_boundary=True)

        for fkey in mesh.faces():

            descendant = {i: j for i, j in subd.face_halfedges(fkey)}
            ancestor = {j: i for i, j in subd.face_halfedges(fkey)}

            x, y, z = mesh.face_centroid(fkey)
            c = subd.add_vertex(x=x, y=y, z=z)

            for key in mesh.face_vertices(fkey):
                a = ancestor[key]
                d = descendant[key]
                subd.add_face([a, key, d, c])

            del subd.face[fkey]

        mesh = subd

    return mesh


def mesh_subdivide_corner(mesh, k=1):
    """Subdivide a mesh by cutting croners.

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

    Returns
    -------
    Mesh
        The subdivided mesh.

    Notes
    -----
    This is essentially the same as Loop subdivision, but applied to general
    meshes.

    """

    for _ in range(k):
        subd = mesh.copy()

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

    return mesh


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
    .. plot::
        :include-source:

        from compas.datastructures import Mesh
        from compas.topology import mesh_subdivide_catmullclark
        from compas.plotters import MeshPlotter

        vertices = [[0., 0., 0.], [1., 0., 0.], [1., 1., 0.], [0., 1.0, 0.]]
        faces = [[0, 1, 2, 3]]

        mesh = Mesh.from_vertices_and_faces(vertices, faces)
        subd = mesh_subdivide_catmullclark(mesh, k=3, fixed=mesh.vertices())

        plotter = MeshPlotter(subd)

        plotter.draw_vertices(facecolor={key: '#ff0000' for key in mesh.vertices()}, radius=0.01)
        plotter.draw_faces()

        plotter.show()


    .. plot::
        :include-source:

        from compas.datastructures import Mesh
        from compas.topology import mesh_subdivide_catmullclark
        from compas.plotters import MeshPlotter

        vertices = [[0., 0., 0.], [1., 0., 0.], [1., 1., 0.], [0., 1.0, 0.]]
        faces = [[0, 1, 2, 3]]

        mesh = Mesh.from_vertices_and_faces(vertices, faces)
        subd = mesh_subdivide_catmullclark(mesh, k=3, fixed=None)

        plotter = MeshPlotter(subd)

        plotter.draw_vertices(facecolor={key: '#ff0000' for key in mesh.vertices()}, radius=0.01)
        plotter.draw_faces()

        plotter.show()


    .. code-block:: python

        from compas.datastructures import Mesh

        from compas.topology import mesh_subdivide_catmullclark
        from compas.geometry import Polyhedron
        from compas.viewers import SubdMeshViewer

        cube = Polyhedron.generate(6)

        mesh = Mesh.from_vertices_and_faces(cube.vertices, cube.faces)

        viewer = SubdMeshViewer(mesh, subdfunc=mesh_subdivide_catmullclark, width=1440, height=900)

        viewer.axes_on = False
        viewer.grid_on = False

        for _ in range(10):
           viewer.camera.zoom_in()

        viewer.subdivide(k=4)

        viewer.setup()
        viewer.show()


    .. figure:: /_images/subdivide_mesh_catmullclark-screenshot.*
        :figclass: figure
        :class: figure-img img-fluid

    """
    if not fixed:
        fixed = []

    fixed = set(fixed)

    for _ in range(k):

        subd = mesh.copy()

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

    return mesh


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

    """
    if not fixed:
        fixed = []

    fixed = set(fixed)

    # cls = type(mesh)

    for _ in range(k):
        old_xyz      = {key: mesh.vertex_coordinates(key) for key in mesh.vertices()}
        fkey_old_new = {fkey: {} for fkey in mesh.faces()}

        # subd = cls()
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

                # fkey_old_new[fkey][old] = subd.add_vertex(x=cx, y=cy, z=cz)
                new = subd.add_vertex(cx, cy, cz)
                fkey_old_new[fkey][old] = new

                face.append(new)

            subd.add_face(face)

        # for fkey in mesh.faces():
        #     subd.add_face([fkey_old_new[fkey][key] for key in mesh.face_vertices(fkey)])

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

    return mesh


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
    .. plot::
        :include-source:

        from compas.datastructures import Mesh
        from compas.topology import trimesh_subdivide_loop
        from compas.plotters import MeshPlotter

        points = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, 1.0, 0.0]]
        faces = [[0, 1, 2]]
        mesh = Mesh.from_vertices_and_faces(points, faces)

        subd = trimesh_subdivide_loop(mesh, k=5)

        plotter = MeshPlotter(subd)
        plotter.draw_vertices(radius=0.002)
        plotter.draw_faces()
        plotter.show()


    .. plot::
        :include-source:

        from compas.datastructures import Mesh
        from compas.topology import trimesh_subdivide_loop
        from compas.topology import delaunay_from_points
        from compas.geometry import pointcloud_xy
        from compas.plotters import MeshPlotter

        points = pointcloud_xy(10, (0, 100))
        faces = delaunay_from_points(points)
        mesh = Mesh.from_vertices_and_faces(points, faces)

        subd = trimesh_subdivide_loop(mesh, k=3)

        plotter = MeshPlotter(subd)
        plotter.draw_vertices(radius=0.1)
        plotter.draw_faces()
        plotter.show()

    """
    if not fixed:
        fixed = []

    fixed = set(fixed)

    subd = mesh.copy()

    for _ in range(k):
        key_xyz       = {key: subd.vertex_coordinates(key) for key in subd.vertices()}
        fkey_vertices = {fkey: subd.face_vertices(fkey)[:] for fkey in subd.faces()}

        uv_w = {(u, v): subd.face_vertex_ancestor(fkey, u) for fkey in subd.faces() for u, v in subd.face_halfedges(fkey)}

        boundary = set(subd.vertices_on_boundary())

        # even vertices
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

                # a = (5. / 8. - (3. / 8. + 0.25 * cos(2 * pi / n)) ** 2) / n

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

    return subd


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    # from functools import partial

    # import compas

    # from compas.datastructures import Mesh
    # from compas.utilities import print_profile
    # from compas.viewers import MeshViewer

    # mesh = Mesh.from_polyhedron(6)
    # # fixed = [mesh.get_any_vertex()]
    # # print(fixed)

    # subdivide = partial(mesh_subdivide_catmullclark)
    # subd = subdivide(mesh, k=4)

    # viewer = MeshViewer()
    # viewer.mesh = subd
    # viewer.show()

    from compas.datastructures import Mesh

    from compas.topology import trimesh_subdivide_loop
    from compas.topology import delaunay_from_points
    from compas.topology import voronoi_from_delaunay

    from compas.geometry import pointcloud_xy

    from compas.plotters import MeshPlotter

    # points = pointcloud_xy(10, (0, 100))
    # faces = delaunay_from_points(points)

    points = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, 1.0, 0.0]]
    faces = [[0, 1, 2]]

    mesh = Mesh.from_vertices_and_faces(points, faces)

    subd = trimesh_subdivide_loop(mesh, k=6)

    plotter = MeshPlotter(subd, figsize=(10, 7))

    # plotter.draw_vertices(radius=0.1)
    plotter.draw_faces()

    plotter.show()
