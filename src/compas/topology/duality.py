from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import circle_from_points_xy
from compas.geometry import angle_vectors
from compas.geometry import is_ccw_xy


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'mesh_dual',
    'network_dual',
    'network_find_faces',
]


def mesh_dual(mesh, cls=None):
    """Construct the dual of a mesh.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.
    cls : Mesh, optional [None]
        The type of the dual mesh.
        Defaults to the type of the provided mesh object.

    Returns
    -------
    Mesh
        The dual mesh object.

    Examples
    --------
    .. plot::
        :include-source:

        import compas
        from compas.datastructures import Mesh
        from compas.topology import mesh_dual
        from compas.plotters import MeshPlotter

        mesh = Mesh.from_obj(compas.get_data('faces.obj'))

        dual = mesh_dual(mesh)

        lines = []
        for u, v in mesh.edges():
            lines.append({
                'start': mesh.vertex_coordinates(u, 'xy'),
                'end'  : mesh.vertex_coordinates(v, 'xy'),
                'color': '#cccccc',
                'width': 1.0
            })

        plotter = MeshPlotter(dual)

        plotter.draw_lines(lines)

        plotter.draw_vertices(facecolor='#eeeeee', edgecolor='#000000', radius=0.2, text='key')
        plotter.draw_edges()

        plotter.show()

    """
    if not cls:
        cls = type(mesh)

    dual = cls()

    fkey_centroid = {fkey: mesh.face_centroid(fkey) for fkey in mesh.faces()}
    outer = mesh.vertices_on_boundary()
    inner = list(set(mesh.vertices()) - set(outer))
    vertices = {}
    faces = {}

    for key in inner:
        fkeys = mesh.vertex_faces(key, ordered=True)
        for fkey in fkeys:
            if fkey not in vertices:
                vertices[fkey] = fkey_centroid[fkey]
        faces[key] = fkeys

    for key, (x, y, z) in vertices.items():
        dual.add_vertex(key, x=x, y=y, z=z)

    for fkey, vertices in faces.items():
        dual.add_face(vertices, fkey=fkey)

    return dual


# def mesh_voronoi(mesh, cls=None, update_coordinates=True):
#     """Construct the Voronoi dual of the triangulation of a set of points.

#     Parameters
#     ----------
#     mesh : Mesh
#         A mesh object.
#     cls : Mesh, optional
#         The type of the dual mesh.
#         Defaults to the type of the provided mesh object.
#     update_coordinates : bool, optional
#         Update the vertex coordinates of the voronoi.
#         Defaults to true.

#     Note
#     ----
#     This function produces a mesh with faces that have the oposite cycle direction
#     of the original mesh.

#     Example
#     -------
#     .. plot::
#         :include-source:

#         from numpy import random
#         from numpy import hstack
#         from numpy import zeros

#         from compas.datastructures import Mesh
#         from compas.topology import mesh_dual
#         from compas.topology import mesh_voronoi
#         from compas.topology import delaunay_from_points
#         from compas.topology import trimesh_remesh

#         from compas.plotters import MeshPlotter

#         points = hstack((10.0 * random.random_sample((10, 2)), zeros((10, 1)))).tolist()
#         mesh = Mesh.from_vertices_and_faces(points, delaunay_from_points(points))

#         trimesh_remesh(mesh, 1.0, allow_boundary_split=True)

#         points = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
#         mesh = Mesh.from_vertices_and_faces(points, delaunay_from_points(points))

#         dual = mesh_voronoi(mesh)

#         lines = []
#         for u, v in mesh.edges():
#             lines.append({
#                 'start': mesh.vertex_coordinates(u, 'xy'),
#                 'end'  : mesh.vertex_coordinates(v, 'xy'),
#                 'color': '#cccccc',
#                 'width': 0.5
#             })

#         plotter = MeshPlotter(dual, figsize=(10, 7))

#         plotter.draw_lines(lines)
#         plotter.draw_vertices(facecolor='#eeeeee', edgecolor='#000000', radius=0.05)
#         plotter.draw_faces(facecolor='#eeeeee', edgecolor='#eeeeee', text='key')
#         plotter.draw_edges(keys=[(u, v) for u, v in dual.edges() if not dual.is_edge_naked(u, v)])

#         plotter.show()

#     """
#     if not cls:
#         cls = type(mesh)

#     fkey_centroid = {fkey: mesh.face_centroid(fkey) for fkey in mesh.faces()}
#     uv_fkey = {}

#     outer = mesh.vertices_on_boundary(ordered=True)[::-1]
#     inner = list(set(mesh.vertices()) - set(outer))

#     f = mesh._get_face_key(None)

#     for i in range(-1, len(outer) - 1):
#         u = outer[i]
#         v = outer[i + 1]
#         uv_fkey[(u, v)] = f
#         fkey_centroid[f] = mesh.edge_midpoint(u, v)
#         f += 1

#     vertices = {}
#     faces = {}

#     for key in inner:
#         fkeys = mesh.vertex_faces(key, ordered=True)
#         for fkey in fkeys:
#             if fkey not in vertices:
#                 vertices[fkey] = fkey_centroid[fkey]
#         faces[key] = fkeys

#     for key in outer:
#         nbrs = mesh.vertex_neighbours(key, ordered=True)

#         if len(nbrs) < 2:
#             continue

#         # the first boundary edge
#         fkey = uv_fkey[(nbrs[0], key)]
#         fkeys = [fkey]
#         if fkey not in vertices:
#             vertices[fkey] = fkey_centroid[fkey]

#         # all internal edges
#         for nbr in nbrs[0:-1]:
#             fkey = mesh.halfedge[nbr][key]
#             fkeys.append(fkey)
#             if fkey not in vertices:
#                 vertices[fkey] = fkey_centroid[fkey]

#         # the last boundary edge
#         fkey = uv_fkey[(key, nbrs[-1])]
#         fkeys.append(fkey)
#         if fkey not in vertices:
#             vertices[fkey] = fkey_centroid[fkey]
#         faces[key] = fkeys

#     voronoi = cls()

#     for key, (x, y, z) in vertices.items():
#         voronoi.add_vertex(key, x=x, y=y, z=z)

#     for fkey, vertices in faces.items():
#         voronoi.add_face(vertices, fkey=fkey)

#     if update_coordinates:
#         for key in mesh.faces():
#             a, b, c = mesh.face_coordinates(key)
#             center, radius, normal = circle_from_points_xy(a, b, c)
#             voronoi.vertex[key]['x'] = center[0]
#             voronoi.vertex[key]['y'] = center[1]
#             voronoi.vertex[key]['z'] = center[2]

#     return voronoi


def network_dual(network, cls=None):
    """Construct the dual of a network.

    Parameters:
        network (compas.datastructures.network.Network): The network object.
        cls (compas.datastructures.network.Network):
            Optional.
            The class of the dual.
            Default is ``None``.
            If ``None``, the cls is inferred from the type of the provided network
            object.

    Warning:
        A network (or a graph) has a dual if, and only if, it is planar.
        Constructing the dual relies on the information about the faces of the
        network, or, in other words, about the ordering of neighbouring vertices
        around a vertex. To determine the faces of the network (using :func:`find_network_faces`)
        the network should be embedded in the plane, i.e drawn such that it is a
        proper cell decomposition of the plane (it divides the plane in non-overlapping
        spaces).

    Example:

        .. plot::
            :include-source:

            import compas

            from compas.topology import FaceNetwork
            from compas.topology import network_find_faces
            from compas.topology import network_dual
            from compas.plotters import NetworkPlotter

            network = FaceNetwork.from_obj(compas.get_data('grid_irregular.obj'))

            network_find_faces(network, breakpoints=network.leaves())

            dual = network_dual(network)

            plotter = NetworkPlotter(dual)

            lines = []
            for u, v in network.edges():
                lines.append({
                    'start': network.vertex_coordinates(u, 'xy'),
                    'end': network.vertex_coordinates(v, 'xy'),
                    'color': '#cccccc'
                })

            points = []
            for key in network.vertices():
                points.append({
                    'pos': network.vertex_coordinates(key, 'xy'),
                    'facecolor': '#ff0000',
                    'edgecolor': '#000000',
                    'radius': 0.075,
                })

            plotter.draw_lines(lines)
            plotter.draw_points(points)
            plotter.draw_vertices(radius=0.15, facecolor='#ffffff', edgecolor='#444444', text={key: key for key in network.vertices()})
            plotter.draw_edges()

            plotter.show()

    """
    if not cls:
        cls = type(network)

    dual = cls()

    for fkey in network.faces():
        x, y, z = network.face_center(fkey)
        dual.add_vertex(fkey, x=x, y=y, z=z)

    # for fkey, vertices in faces.items():
    #     dual.add_face(vertices, fkey=fkey)

    for u, v in network.edges():
        f1 = network.halfedge[u][v]
        f2 = network.halfedge[v][u]

        if f1 is not None and f2 is not None:
            dual.add_edge(f1, f2)

    return dual


def network_find_faces(network, breakpoints=None):
    """Find the faces of a network.

    Parameters:
        network (compas.datastructures.network.Network): The network object.
        breakpoints (list): Optional.
            The vertices at which to break the found faces.
            Default is ``None``.

    Notes:
        ``breakpoints`` are primarily used to break up the outside face in between
        specific vertices. For example, in structural applications involving dual
        diagrams, any vertices where external forces are applied (loads or reactions)
        should be input as breakpoints.


    Warning:
        This algorithms is essentially a wall follower (a type of maze-solving algorithm).
        It relies on the geometry of the network to be repesented as a planar,
        straight-line embedding. It determines an ordering of the neighbouring vertices
        around each vertex, and then follows the *walls* of the network, always
        taking turns in the same direction.

    Example:

        Compare the faces on the plots of the same network, with and without
        breakpoints at the leaves.

        Note that with the breakpoints, face ``0`` (the outside face) no longer exists.
        Breaking up the face at the breakpoints happens after all faces have been
        found. Therefore, numbering of the faces replacing the outside face starts
        from the highest number of the faces found initially.


        .. plot::
            :include-source:

            # no breakpoints

            import compas
            from compas.topology import FaceNetwork
            from compas.topology import network_find_faces
            from compas.plotters import FaceNetworkPlotter

            network = FaceNetwork.from_obj(compas.get_data('grid_irregular.obj'))

            network_find_faces(network)

            plotter = FaceNetworkPlotter(network)

            plotter.draw_vertices(
                radius=0.075,
                facecolor={key: '#cccccc' for key in network.leaves()}
            )
            plotter.draw_edges(
                color={(u, v): '#cccccc' for u, v in network.edges()}
            )
            plotter.draw_faces(
                facecolor={fkey: '#eeeeee' for fkey in network.faces()},
                text={fkey: fkey for fkey in network.faces()}
            )

            plotter.show()

        .. plot::
            :include-source:

            # leaves as breakpoints

            import compas
            from compas.topology import FaceNetwork
            from compas.topology import network_find_faces
            from compas.plotters import FaceNetworkPlotter

            network = FaceNetwork.from_obj(compas.get_data('grid_irregular.obj'))

            network_find_faces(network, breakpoints=network.leaves())

            plotter = FaceNetworkPlotter(network)

            plotter.draw_vertices(
                radius=0.075,
                facecolor={key: '#cccccc' for key in network.leaves()}
            )
            plotter.draw_edges(
                color={(u, v): '#cccccc' for u, v in network.edges()}
            )
            plotter.draw_faces(
                facecolor={fkey: '#eeeeee' for fkey in network.faces()},
                text={fkey: fkey for fkey in network.faces()}
            )

            plotter.show()

    """
    if not breakpoints:
        breakpoints = []

    network.clear_facedict()
    network.clear_halfedgedict()

    network.halfedge = {key: {} for key in network.vertices()}

    for u, v in network.edges():
        network.halfedge[u][v] = None
        network.halfedge[v][u] = None

    _sort_neighbours(network)

    leaves = network.leaves()

    if leaves:
        u = sorted([(key, network.vertex[key]) for key in leaves], key=lambda x: (x[1]['y'], x[1]['x']))[0][0]
    else:
        u = sorted(network.vertices(True), key=lambda x: (x[1]['y'], x[1]['x']))[0][0]

    v = _find_first_neighbour(u, network)

    _find_edge_face(u, v, network)

    for u, v in network.edges():
        if network.halfedge[u][v] is None:
            _find_edge_face(u, v, network)
        if network.halfedge[v][u] is None:
            _find_edge_face(v, u, network)

    _break_faces(network, breakpoints)

    return network.face


def _find_first_neighbour(key, network):
    angles = []
    nbrs = list(network.halfedge[key].keys())
    if len(nbrs) == 1:
        return nbrs[0]
    vu = [-1, -1, 0]
    for nbr in nbrs:
        w = [network.vertex[nbr][_] for _ in 'xyz']
        v = [network.vertex[key][_] for _ in 'xyz']
        vw = [w[0] - v[0], w[1] - v[1], 0]
        angles.append(angle_vectors(vu, vw))
    return nbrs[angles.index(min(angles))]


def _sort_neighbours(network, ccw=True):
    sorted_neighbours = {}
    xyz = {key: network.vertex_coordinates(key) for key in network.vertices()}
    for key in network.vertices():
        nbrs = network.vertex_neighbours(key)
        sorted_neighbours[key] = _sort_vertex_neighbours(key, nbrs, xyz, ccw=ccw)
    for key, nbrs in sorted_neighbours.items():
        network.vertex[key]['sorted_neighbours'] = nbrs[::-1]
    return sorted_neighbours


def _sort_vertex_neighbours(key, nbrs, xyz, ccw=True):
    if len(nbrs) == 1:
        return nbrs
    ordered = nbrs[0:1]
    a = xyz[key]
    for i, nbr in enumerate(nbrs[1:]):
        c = xyz[nbr]
        pos = 0
        b = xyz[ordered[pos]]
        while not is_ccw_xy(a, b, c):
            pos += 1
            if pos > i:
                break
            b = xyz[ordered[pos]]
        if pos == 0:
            pos = -1
            b = xyz[ordered[pos]]
            while is_ccw_xy(a, b, c):
                pos -= 1
                if pos < -len(ordered):
                    break
                b = xyz[ordered[pos]]
            pos += 1
        ordered.insert(pos, nbr)
    if not ccw:
        return ordered[::-1]
    return ordered


def _find_edge_face(u, v, network):
    cycle = [u]
    while True:
        cycle.append(v)
        nbrs = network.vertex[v]['sorted_neighbours']
        nbr = nbrs[nbrs.index(u) - 1]
        u, v = v, nbr
        if v == cycle[0]:
            # cycle.append(v)
            break
    fkey = network.add_face(cycle)
    return fkey


def _break_faces(network, breakpoints):
    breakpoints = set(breakpoints)

    for fkey in list(network.faces()):
        vertices = network.face_vertices(fkey)

        faces = []
        faces.append([vertices[0]])
        for i in range(1, len(vertices) - 1):
            key = vertices[i]
            faces[-1].append(key)
            if key in breakpoints:
                faces.append([key])

        faces[-1].append(vertices[-1])
        faces[-1].append(vertices[0])

        if len(faces) == 1:
            continue

        if faces[0][0] not in breakpoints and faces[-1][-1] not in breakpoints:
            if faces[0][0] == faces[-1][-1]:
                faces[:] = [faces[-1] + faces[0][1:]] + faces[1:-1]

        if len(faces) == 1:
            continue

        del network.face[fkey]

        if fkey in network.facedata:
            del network.facedata[fkey]

        for vertices in faces:
            network.add_face(vertices)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from numpy import random
    from numpy import hstack
    from numpy import zeros

    from compas.datastructures import Mesh
    from compas.datastructures import FaceNetwork

    from compas.topology import mesh_dual
    from compas.topology import network_dual
    from compas.topology import delaunay_from_points
    from compas.topology import trimesh_remesh

    from compas.plotters import MeshPlotter

    points = hstack((10.0 * random.random_sample((10, 2)), zeros((10, 1)))).tolist()
    faces = delaunay_from_points(points)
    mesh = Mesh.from_vertices_and_faces(points, faces)

    trimesh_remesh(mesh, 1.0, allow_boundary_split=True)

    points = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
    faces = delaunay_from_points(points)
    mesh = Mesh.from_vertices_and_faces(points, faces)

    dual = mesh_dual(mesh)

    # network = FaceNetwork.from_vertices_and_faces(points, faces)
    # network_find_faces(network)
    # dual = network_dual(network)

    lines = []
    for u, v in mesh.edges():
        lines.append({
            'start': mesh.vertex_coordinates(u, 'xy'),
            'end'  : mesh.vertex_coordinates(v, 'xy'),
            'color': '#cccccc',
            'width': 0.5
        })

    plotter = MeshPlotter(dual, figsize=(10, 7))

    plotter.draw_lines(lines)
    plotter.draw_vertices(facecolor='#eeeeee', edgecolor='#000000', radius=0.05)
    plotter.draw_faces(facecolor='#eeeeee', edgecolor='#eeeeee', text='key')
    plotter.draw_edges()

    plotter.show()
