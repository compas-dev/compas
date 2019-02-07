from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import random

from compas.geometry import centroid_points
from compas.geometry import distance_point_point
from compas.geometry import add_vectors
from compas.geometry import bounding_box

from compas.geometry import is_point_in_polygon_xy
from compas.geometry import is_point_in_triangle_xy
from compas.geometry import is_point_in_circle_xy
from compas.geometry import circle_from_points_xy


__all__ = [
    'delaunay_from_points',
]


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

        from compas.datastructures import Mesh
        from compas.geometry import pointcloud_xy
        from compas.geometry import delaunay_from_points
        from compas.plotters import MeshPlotter

        points = pointcloud_xy(20, (0, 50))
        faces = delaunay_from_points(points)

        delaunay = Mesh.from_vertices_and_faces(points, faces)

        plotter = MeshPlotter(delaunay)
        plotter.draw_vertices(radius=0.1)
        plotter.draw_faces()
        plotter.show()

    """
    from compas.datastructures import Mesh
    from compas.datastructures import trimesh_swap_edge

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
                    fkey, fkey_op = trimesh_swap_edge(mesh, u, v)
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


# def voronoi_from_delaunay(delaunay):
#     """Construct the Voronoi dual of the triangulation of a set of points.

#     Parameters
#     ----------
#     delaunay : Mesh
#         A delaunay mesh.

#     Returns
#     -------
#     Mesh
#         The corresponding voronoi mesh.

#     Warning
#     -------
#     This function does not work properly if all vertices of the delaunay
#     are on the boundary.

#     Example
#     -------
#     .. plot::
#         :include-source:

#         from compas.datastructures import Mesh
#         from compas.datastructures import trimesh_remesh
#         from compas.geometry import delaunay_from_points
#         from compas.geometry import voronoi_from_delaunay
#         from compas.geometry import pointcloud_xy
#         from compas.plotters import MeshPlotter

#         points = pointcloud_xy(10, (0, 10))
#         faces = delaunay_from_points(points)
#         delaunay = Mesh.from_vertices_and_faces(points, faces)

#         trimesh_remesh(delaunay, 1.0, allow_boundary_split=True)

#         points = [delaunay.vertex_coordinates(key) for key in delaunay.vertices()]
#         faces = delaunay_from_points(points)
#         delaunay = Mesh.from_vertices_and_faces(points, faces)

#         voronoi = voronoi_from_delaunay(delaunay)

#         lines = []
#         for u, v in voronoi.edges():
#             lines.append({
#                 'start': voronoi.vertex_coordinates(u, 'xy'),
#                 'end'  : voronoi.vertex_coordinates(v, 'xy'),
#                 'width': 1.0
#             })

#         plotter = MeshPlotter(delaunay)

#         plotter.draw_lines(lines)

#         plotter.draw_vertices(
#             radius=0.075,
#             facecolor={key: '#0092d2' for key in delaunay.vertices() if key not in delaunay.vertices_on_boundary()})

#         plotter.draw_edges(color='#cccccc')

#         plotter.show()

#     """
#     voronoi = mesh_dual(delaunay)

#     for key in voronoi.vertices():
#         a, b, c = delaunay.face_coordinates(key)
#         center, radius, normal = circle_from_points_xy(a, b, c)
#         voronoi.vertex[key]['x'] = center[0]
#         voronoi.vertex[key]['y'] = center[1]
#         voronoi.vertex[key]['z'] = center[2]

#     return voronoi


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.datastructures import Mesh
    from compas.geometry import pointcloud_xy
    from compas.geometry import delaunay_from_points
    from compas.plotters import MeshPlotter

    points = pointcloud_xy(20, (0, 50))
    faces = delaunay_from_points(points)

    delaunay = Mesh.from_vertices_and_faces(points, faces)

    plotter = MeshPlotter(delaunay, figsize=(12, 8))

    plotter.draw_vertices(radius=0.1)
    plotter.draw_faces()

    plotter.show()
