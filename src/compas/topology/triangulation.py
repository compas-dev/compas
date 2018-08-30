from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import random

from compas.utilities import flatten

from compas.geometry import centroid_points
from compas.geometry import distance_point_point
from compas.geometry import add_vectors
from compas.geometry import bounding_box

from compas.geometry import is_point_in_polygon_xy
from compas.geometry import is_point_in_triangle_xy
from compas.geometry import is_point_in_circle_xy
from compas.geometry import circle_from_points_xy

from compas.geometry import mesh_smooth_area

from compas.topology import mesh_dual


__all__ = [
    'mesh_quads_to_triangles',
    'delaunay_from_points',
    'voronoi_from_delaunay',
    'trimesh_remesh',
]


def mesh_quads_to_triangles(mesh, check_angles=False):
    """"""
    for fkey in list(mesh.faces()):
        vertices = mesh.face_vertices(fkey)
        if len(vertices) == 4:
            a, b, c, d = vertices
            mesh.split_face(fkey, b, d)


def delaunay_from_points(points, boundary=None, holes=None, tiny=1e-12):
    """Computes the delaunay triangulation for a list of points.

    Parameters
    ----------
    points : sequence of tuple
        XYZ coordinates of the original points.
    boundary : sequence of tuples
        list of ordered points describing the outer boundary (optional)
    holes : list of sequences of tuples
        list of polygons (ordered points describing internal holes (optional)

    Returns
    -------
    list
        The faces of the triangulation.
        Each face is a triplet of indices referring to the list of point coordinates.

    Notes
    -----
    For more info, see [1]_.

    References
    ----------
    .. [1] Sloan, S. W., 1987 *A fast algorithm for constructing Delaunay triangulations in the plane*
           Advances in Engineering Software 9(1): 34-55, 1978.

    Example
    -------
    .. plot::
        :include-source:

        from compas.geometry import pointcloud_xy
        from compas.datastructures import Mesh
        from compas.topology import delaunay_from_points
        from compas.plotters import MeshPlotter

        points = pointcloud_xy(10, (0, 10))
        faces = delaunay_from_points(points)

        delaunay = Mesh.from_vertices_and_faces(points, faces)

        plotter = MeshPlotter(delaunay)

        plotter.draw_vertices(radius=0.1)
        plotter.draw_faces()

        plotter.show()

    """
    from compas.datastructures import Mesh

    def super_triangle(coords):
        centpt = centroid_points(coords)
        bbpts  = bounding_box(coords)
        dis    = distance_point_point(bbpts[0], bbpts[2])
        dis    = dis * 300
        v1     = (0 * dis, 2 * dis, 0)
        v2     = (1.73205 * dis, -1.0000000000001 * dis, 0)  # due to numerical issues
        v3     = (-1.73205 * dis, -1 * dis, 0)
        pt1    = add_vectors(centpt, v1)
        pt2    = add_vectors(centpt, v2)
        pt3    = add_vectors(centpt, v3)
        return pt1, pt2, pt3

    mesh = Mesh()

    # to avoid numerical issues for perfectly structured point sets
    points = [(point[0] + random.uniform(-tiny, tiny), point[1] + random.uniform(-tiny, tiny), 0.0) for point in points]

    # create super triangle
    pt1, pt2, pt3 = super_triangle(points)

    # add super triangle vertices to mesh
    n = len(points)
    super_keys = n, n + 1, n + 2

    mesh.add_vertex(super_keys[0], {'x': pt1[0], 'y': pt1[1], 'z': pt1[2]})
    mesh.add_vertex(super_keys[1], {'x': pt2[0], 'y': pt2[1], 'z': pt2[2]})
    mesh.add_vertex(super_keys[2], {'x': pt3[0], 'y': pt3[1], 'z': pt3[2]})

    mesh.add_face(super_keys)

    # iterate over points
    for i, pt in enumerate(points):
        key = i

        # newtris should be intialised here

        # check in which triangle this point falls
        for fkey in list(mesh.faces()):
            # abc = mesh.face_coordinates(fkey) #This is slower
            # This is faster:
            keya, keyb, keyc = mesh.face_vertices(fkey)

            dicta = mesh.vertex[keya]
            dictb = mesh.vertex[keyb]
            dictc = mesh.vertex[keyc]

            a = [dicta['x'], dicta['y']]
            b = [dictb['x'], dictb['y']]
            c = [dictc['x'], dictc['y']]

            if is_point_in_triangle_xy(pt, [a, b, c], True):
                # generate 3 new triangles (faces) and delete surrounding triangle
                key, newtris = mesh.insert_vertex(fkey, key=key, xyz=pt, return_fkeys=True)
                break

        while newtris:
            fkey = newtris.pop()

            # get opposite_face
            keys  = mesh.face_vertices(fkey)
            s     = list(set(keys) - set([key]))
            u, v  = s[0], s[1]
            fkey1 = mesh.halfedge[u][v]

            if fkey1 != fkey:
                fkey_op, u, v = fkey1, u, v
            else:
                fkey_op, u, v = mesh.halfedge[v][u], u, v

            if fkey_op:
                keya, keyb, keyc = mesh.face_vertices(fkey_op)
                dicta = mesh.vertex[keya]
                a = [dicta['x'], dicta['y']]
                dictb = mesh.vertex[keyb]
                b = [dictb['x'], dictb['y']]
                dictc = mesh.vertex[keyc]
                c = [dictc['x'], dictc['y']]

                circle = circle_from_points_xy(a, b, c)

                if is_point_in_circle_xy(pt, circle):
                    fkey, fkey_op = mesh.swap_edge_tri(u, v)
                    newtris.append(fkey)
                    newtris.append(fkey_op)

    # Delete faces adjacent to supertriangle
    for key in super_keys:
        mesh.delete_vertex(key)

    # Delete faces outside of boundary
    if boundary:
        for fkey in list(mesh.faces()):
            centroid = mesh.face_centroid(fkey)
            if not is_point_in_polygon_xy(centroid, boundary):
                mesh.delete_face(fkey)

    # Delete faces inside of inside boundaries
    if holes:
        for polygon in holes:
            for fkey in list(mesh.faces()):
                centroid = mesh.face_centroid(fkey)
                if is_point_in_polygon_xy(centroid, polygon):
                    mesh.delete_face(fkey)

    return [mesh.face_vertices(fkey) for fkey in mesh.faces()]


def delaunay_from_points_numpy(points):
    """"""
    from numpy import asarray
    from scipy.spatial import Delaunay

    xyz = asarray(points)
    d = Delaunay(xyz[:, 0:2])
    return d.simplices


def voronoi_from_points_numpy(points):
    """Generate a voronoi diagram from a set of points.

    Parameters
    ----------
    points : list of list of float
        XYZ coordinates of the voronoi sites.

    Returns
    -------

    Examples
    --------
    .. code-block:: python

        from compas.datastructures import Mesh
        from compas.plotters import MeshPlotter
        from compas.geometry import closest_point_on_line_xy
        from compas.topology.triangulation import voronoi_from_points_numpy

        mesh = Mesh()

        mesh.add_vertex(x=0, y=0)
        mesh.add_vertex(x=1.5, y=0)
        mesh.add_vertex(x=1, y=1)
        mesh.add_vertex(x=0, y=2)

        mesh.add_face([0, 1, 2, 3])

        sites = mesh.get_vertices_attributes('xy')
        voronoi = voronoi_from_points_numpy(sites)

        points = []
        for xy in voronoi.vertices:
            points.append({
                'pos'       : xy,
                'radius'    : 0.02,
                'facecolor' : '#ff0000',
                'edgecolor' : '#ffffff',
            })

        lines = []
        arrows = []
        for (a, b), (c, d) in zip(voronoi.ridge_vertices, voronoi.ridge_points):
            if a > -1 and b > -1:
                lines.append({
                    'start' : voronoi.vertices[a],
                    'end'   : voronoi.vertices[b],
                    'width' : 1.0,
                    'color' : '#ff0000',
                })
            elif a == -1:
                sp = voronoi.vertices[b]
                ep = closest_point_on_line_xy(sp, (voronoi.points[c], voronoi.points[d]))
                arrows.append({
                    'start' : sp,
                    'end'   : ep,
                    'width' : 1.0,
                    'color' : '#00ff00',
                    'arrow' : 'end'
                })
            else:
                sp = voronoi.vertices[a]
                ep = closest_point_on_line_xy(sp, (voronoi.points[c], voronoi.points[d]))
                arrows.append({
                    'start' : sp,
                    'end'   : ep,
                    'width' : 1.0,
                    'color' : '#00ff00',
                    'arrow' : 'end'
                })


        plotter = MeshPlotter(mesh, figsize=(10, 7))
        plotter.draw_points(points)
        plotter.draw_lines(lines)
        plotter.draw_arrows(arrows)
        plotter.draw_vertices(radius=0.02)
        plotter.draw_faces()
        plotter.show()    

    """
    from numpy import asarray
    from scipy.spatial import Voronoi
    points = asarray(points)
    voronoi = Voronoi(points)
    return voronoi


def voronoi_from_delaunay(delaunay):
    """Construct the Voronoi dual of the triangulation of a set of points.

    Parameters
    ----------
    delaunay : Mesh
        A delaunay mesh.

    Returns
    -------
    Mesh
        The corresponding voronoi mesh.

    Warning
    -------
    This function does not work properly if all vertices of the delaunay
    are on the boundary.

    Example
    -------
    .. plot::
        :include-source:

        from compas.datastructures import Mesh
        from compas.topology import trimesh_remesh
        from compas.topology import delaunay_from_points
        from compas.topology import voronoi_from_delaunay

        from compas.geometry import pointcloud_xy

        from compas.plotters import MeshPlotter

        points = pointcloud_xy(10, (0, 10))
        faces = delaunay_from_points(points)
        delaunay = Mesh.from_vertices_and_faces(points, faces)

        trimesh_remesh(delaunay, 1.0, allow_boundary_split=True)

        points = [delaunay.vertex_coordinates(key) for key in delaunay.vertices()]
        faces = delaunay_from_points(points)
        delaunay = Mesh.from_vertices_and_faces(points, faces)

        voronoi  = voronoi_from_delaunay(delaunay)

        lines = []
        for u, v in voronoi.edges():
            lines.append({
                'start': voronoi.vertex_coordinates(u, 'xy'),
                'end'  : voronoi.vertex_coordinates(v, 'xy'),
                'width': 1.0
            })

        plotter = MeshPlotter(delaunay, figsize=(10, 6))

        plotter.draw_lines(lines)

        plotter.draw_vertices(
            radius=0.075,
            facecolor={key: '#0092d2' for key in delaunay.vertices() if key not in delaunay.vertices_on_boundary()})

        plotter.draw_edges(color='#cccccc')

        plotter.show()

    """
    voronoi = mesh_dual(delaunay)

    for key in voronoi.vertices():
        a, b, c = delaunay.face_coordinates(key)
        center, radius, normal = circle_from_points_xy(a, b, c)
        voronoi.vertex[key]['x'] = center[0]
        voronoi.vertex[key]['y'] = center[1]
        voronoi.vertex[key]['z'] = center[2]

    return voronoi


def trimesh_remesh(mesh,
                   target,
                   kmax=100,
                   tol=0.1,
                   divergence=0.01,
                   verbose=False,
                   allow_boundary_split=False,
                   allow_boundary_swap=False,
                   allow_boundary_collapse=False,
                   smooth=True,
                   fixed=None,
                   callback=None,
                   callback_args=None):
    """Remesh until all edges have a specified target length.

    Parameters
    ----------
    mesh : Mesh
        A triangle mesh.
    target : float
        The target length for the mesh edges.
    kmax : int, optional [100]
        The number of iterations.
    tol : float, optional [0.1]
        Length deviation tolerance.
    divergence : float, optional [0.01]
        ??
    verbose : bool, optional [False]
        Print feedback messages.
    allow_boundary_split : bool, optional [False]
        Allow boundary edges to be split.
    allow_boundary_swap : bool, optional [False]
        Allow boundary edges or edges connected to the boundary to be swapped.
    allow_boundary_collapse : bool, optional [False]
        Allow boundary edges or edges connected to the boundary to be collapsed.
    smooth : bool, optional [True]
        Apply smoothing at every iteration.
    fixed : list, optional [None]
        A list of vertices that have to stay fixed.
    callback : callable, optional [None]
        A user-defined function that is called after every iteration.
    callback_args : list, optional [None]
        A list of additional parameters to be passed to the callback function.

    Returns
    -------
    None

    Notes
    -----
    This algorithm not only changes the geometry of the mesh, but also its
    topology as needed to achieve the specified target lengths.
    Topological changes are made such that vertex valencies are well-balanced
    and close to six. This involves three operations:

        * split edges that are longer than a maximum length,
        * collapse edges that are shorter than a minimum length,
        * swap edges if this improves the valency error.

    The minimum and maximum lengths are calculated based on a desired target
    length.

    For more info, see [1]_.

    References
    ----------
    .. [1] Botsch, M. & Kobbelt, L., 2004. *A remeshing approach to multiresolution modeling*.
           Proceedings of the 2004 Eurographics/ACM SIGGRAPH symposium on Geometry processing - SGP '04, p.185.
           Available at: http://portal.acm.org/citation.cfm?doid=1057432.1057457.

    Warning
    -------
    In the current implementation, allowing boundary collapses may lead to unexpected
    results since it will not preserve the gometry of the original boundary.

    Examples
    --------
    .. plot::
        :include-source:

        from compas.datastructures import Mesh
        from compas.plotters import MeshPlotter
        from compas.topology import trimesh_remesh

        vertices = [
            (0.0, 0.0, 0.0),
            (10.0, 0.0, 0.0),
            (10.0, 10.0, 0.0),
            (0.0, 10.0, 0.0),
            (5.0, 5.0, 0.0)
        ]
        faces = [
            (0, 1, 4),
            (1, 2, 4),
            (2, 3, 4),
            (3, 0, 4)
        ]

        mesh = Mesh.from_vertices_and_faces(vertices, faces)

        trimesh_remesh(
            mesh,
            target=0.5,
            tol=0.05,
            kmax=300,
            allow_boundary_split=True,
            allow_boundary_swap=True,
            verbose=False
        )

        plotter = MeshPlotter(mesh)

        plotter.draw_vertices(radius=0.03)
        plotter.draw_faces()
        plotter.draw_edges()

        plotter.show()

    See Also
    --------
    * :func:`compas.geometry.smooth_area`

    """
    if verbose:
        print(target)

    lmin = (1 - tol) * (4.0 / 5.0) * target
    lmax = (1 + tol) * (4.0 / 3.0) * target

    edge_lengths = [mesh.edge_length(u, v) for u, v in mesh.edges()]
    target_start = max(edge_lengths) / 2.0

    fac = target_start / target

    boundary = set(mesh.vertices_on_boundary())

    fixed = fixed or []
    fixed = set(fixed)

    count = 0

    kmax_start = kmax / 2.0

    for k in range(kmax):

        if k <= kmax_start:
            scale = fac * (1.0 - k / kmax_start)
            dlmin = lmin * scale
            dlmax = lmax * scale
        else:
            dlmin = 0
            dlmax = 0

        if verbose:
            print(k)

        count += 1

        if k % 20 == 0:
            num_vertices_1 = mesh.number_of_vertices()

        # split
        if count == 1:
            visited = set()

            for u, v in list(mesh.edges()):
                if u in visited or v in visited:
                    continue
                if mesh.edge_length(u, v) <= lmax + dlmax:
                    continue

                if verbose:
                    print('split edge: {0} - {1}'.format(u, v))

                mesh.split_edge_tri(u, v, allow_boundary=allow_boundary_split)

                visited.add(u)
                visited.add(v)

        # collapse
        elif count == 2:
            visited = set()

            for u, v in list(mesh.edges()):
                if u in visited or v in visited:
                    continue
                if mesh.edge_length(u, v) >= lmin - dlmin:
                    continue
                if verbose:
                    print('collapse edge: {0} - {1}'.format(u, v))

                mesh.collapse_edge_tri(u, v, allow_boundary=allow_boundary_collapse, fixed=fixed)

                visited.add(u)
                visited.add(v)

                visited.update(mesh.halfedge[u])

        # swap
        elif count == 3:
            visited = set()

            for u, v in list(mesh.edges()):
                if u in visited or v in visited:
                    continue

                f1 = mesh.halfedge[u][v]
                f2 = mesh.halfedge[v][u]

                if f1 is None or f2 is None:
                    continue

                face1 = mesh.face[f1]
                face2 = mesh.face[f2]

                v1 = face1[face1.index(u) - 1]
                v2 = face2[face2.index(v) - 1]

                valency1 = mesh.vertex_degree(u)
                valency2 = mesh.vertex_degree(v)
                valency3 = mesh.vertex_degree(v1)
                valency4 = mesh.vertex_degree(v2)

                if u in boundary:
                    valency1 += 2
                if v in boundary:
                    valency2 += 2
                if v1 in boundary:
                    valency3 += 2
                if v2 in boundary:
                    valency4 += 2

                current_error = abs(valency1 - 6) + abs(valency2 - 6) + abs(valency3 - 6) + abs(valency4 - 6)
                flipped_error = abs(valency1 - 7) + abs(valency2 - 7) + abs(valency3 - 5) + abs(valency4 - 5)

                if current_error <= flipped_error:
                    continue

                if verbose:
                    print('swap edge: {0} - {1}'.format(u, v))

                mesh.swap_edge_tri(u, v, allow_boundary=allow_boundary_swap)

                visited.add(u)
                visited.add(v)
        # count
        else:
            count = 0

        if (k - 10) % 20 == 0:
            num_vertices_2 = mesh.number_of_vertices()

            if abs(1 - num_vertices_1 / num_vertices_2) < divergence and k > kmax_start:
                break

        # smoothen
        if smooth:
            if allow_boundary_split:
                boundary = set(mesh.vertices_on_boundary())

            mesh_smooth_area(mesh, fixed=fixed.union(boundary), kmax=1)

        # callback
        if callback:
            callback(mesh, k, callback_args)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    testrun = 2

    if testrun == 1:
        from compas.datastructures import Mesh
        from compas.geometry import pointcloud_xy
        from compas.plotters import MeshPlotter

        points = pointcloud_xy(10, (0, 10))
        faces = delaunay_from_points(points)
        mesh = Mesh.from_vertices_and_faces(points, faces)

        trimesh_remesh(mesh, 1.0, kmax=300, allow_boundary_split=True)

        points = [mesh.vertex_coordinates(key) for key in mesh.vertices()]

        faces = delaunay_from_points(points)
        mesh = Mesh.from_vertices_and_faces(points, faces)

        voronoi  = voronoi_from_delaunay(mesh)

        lines = []
        for u, v in voronoi.edges():
            lines.append({
                'start': voronoi.vertex_coordinates(u, 'xy'),
                'end'  : voronoi.vertex_coordinates(v, 'xy'),
                'width': 1.0
            })

        plotter = MeshPlotter(mesh, figsize=(10, 7))

        plotter.draw_lines(lines)

        plotter.draw_vertices(
            radius=0.075,
            facecolor={key: '#0092d2' for key in mesh.vertices() if key not in mesh.vertices_on_boundary()})

        plotter.draw_edges(color='#cccccc')

        plotter.show()

    if testrun == 2:
        from compas.datastructures import Mesh
        from compas.plotters import MeshPlotter
        from compas.geometry import mesh_smooth_area

        vertices = [(0.0, 0.0, 0.0), (10.0, 0.0, 0.0), (10.0, 10.0, 0.0), (0.0, 10.0, 0.0)]
        faces = [[0, 1, 2, 3]]

        mesh = Mesh.from_vertices_and_faces(vertices, faces)

        key = mesh.insert_vertex(0)
        fixed = [key]

        plotter = MeshPlotter(mesh, figsize=(10, 7))

        plotter.draw_edges(width=0.5)

        def callback(mesh, k, args):
            print(k)
            plotter.update_edges()
            plotter.update()

        trimesh_remesh(
            mesh,
            1.0,
            kmax=200,
            allow_boundary_split=True,
            allow_boundary_swap=True,
            allow_boundary_collapse=False,
            fixed=fixed,
            callback=callback)

        mesh_smooth_area(mesh, fixed=mesh.vertices_on_boundary())

        plotter.update_edges()
        plotter.update(pause=2.0)
        plotter.show()

    if testrun == 3:
        from compas.geometry import pointcloud_xy
        from compas.datastructures import Mesh
        from compas.topology import delaunay_from_points
        from compas.plotters import MeshPlotter

        points = pointcloud_xy(10, (0, 10))
        faces = delaunay_from_points(points)

        delaunay = Mesh.from_vertices_and_faces(points, faces)

        plotter = MeshPlotter(delaunay)

        plotter.draw_vertices(radius=0.1)
        plotter.draw_faces()

        plotter.show()
