import random

from compas.datastructures.mesh import Mesh

from compas.datastructures.mesh.algorithms import mesh_dual
from compas.datastructures.mesh.algorithms import trimesh_optimise_topology
from compas.datastructures.mesh.operations import trimesh_swap_edge
from compas.datastructures.mesh.operations import mesh_split_face

from compas.geometry import centroid_points
from compas.geometry import distance_point_point
from compas.geometry import add_vectors
from compas.geometry import bounding_box
from compas.geometry import circle_from_points

from compas.geometry import is_point_in_polygon_xy
from compas.geometry import is_point_in_triangle_xy
from compas.geometry import is_point_in_circle_xy
from compas.geometry import circle_from_points_xy


__author__    = 'Matthias Rippmann, Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'rippmann@ethz.ch, vanmelet@ethz.ch'


__all__ = [
    'mesh_quads_to_triangles',
    'mesh_delaunay_from_points',
    'mesh_voronoi_from_points'
]


def mesh_quads_to_triangles(mesh, check_angles=False):
    """"""
    for fkey in list(mesh.faces()):
        vertices = mesh.face_vertices(fkey)
        if len(vertices) == 4:
            a, b, c, d = vertices
            mesh_split_face(mesh, fkey, b, d)


def mesh_delaunay_from_points(points, polygon=None, polygons=None):
    """Computes the delaunay triangulation for a list of points.

    Parameters:
        points (sequence of tuple): XYZ coordinates of the original points.
        polygon (sequence of tuples): list of ordered points describing the outer boundary (optional)
        polygons (list of sequences of tuples): list of polygons (ordered points describing internal holes (optional)

    Returns:
        list of lists: list of faces (face = list of vertex indices as integers)

    References:
        Sloan, S. W. (1987) A fast algorithm for constructing Delaunay triangulations in the plane

    Example:

        .. plot::
            :include-source:

            import compas
            from compas.datastructures import Mesh
            from compas.datastructures import mesh_delaunay_from_points

            from compas.visualization import MeshPlotter

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))

            vertices = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
            faces = mesh_delaunay_from_points(vertices)

            delaunay = Mesh.from_vertices_and_faces(vertices, faces)

            plotter = MeshPlotter(delaunay)

            plotter.draw_vertices(radius=0.1)
            plotter.draw_faces()

            plotter.show()

    """
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
    tiny = 1e-8
    pts  = [(point[0] + random.uniform(-tiny, tiny), point[1] + random.uniform(-tiny, tiny), 0.0) for point in points]

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
    for i, pt in enumerate(pts):
        key = i

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

            if is_point_in_triangle_xy(pt, [a, b, c]):
                # generate 3 new triangles (faces) and delete surrounding triangle
                newtris = mesh.insert_vertex(fkey, key=key, xyz=pt)
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
        mesh.remove_vertex(key)

    # Delete faces outside of boundary
    if polygon:
        for fkey in list(mesh.faces()):
            cent = mesh.face_centroid(fkey)
            if not is_point_in_polygon_xy(cent, polygon):
                mesh.delete_face(fkey)

    # Delete faces inside of inside boundaries
    if polygons:
        for polygon in polygons:
            for fkey in list(mesh.faces()):
                cent = mesh.face_centroid(fkey)
                if is_point_in_polygon_xy(cent, polygon):
                    mesh.delete_face(fkey)

    return [[int(key) for key in mesh.face_vertices(fkey, True)] for fkey in mesh.faces()]


def mesh_voronoi_from_points(points, boundary=None, holes=None, return_delaunay=False):
    """Construct the Voronoi dual of the triangulation of a set of points.

    Parameters:
        points
        boundary
        holes
        return_delaunay

    Example:

        .. plot::
            :include-source:

            from numpy import random
            from numpy import hstack
            from numpy import zeros

            from compas.datastructures import Mesh
            from compas.datastructures import trimesh_optimise_topology
            from compas.datastructures import mesh_delaunay_from_points
            from compas.datastructures import mesh_voronoi_from_points
            from compas.visualization import MeshPlotter

            points = hstack((10.0 * random.random_sample((20, 2)), zeros((20, 1)))).tolist()
            mesh = Mesh.from_vertices_and_faces(points, mesh_delaunay_from_points(points))

            trimesh_optimise_topology(mesh, 1.0, allow_boundary_split=True)

            points = [mesh.vertex_coordinates(key) for key in mesh.vertices()]

            voronoi, delaunay = mesh_voronoi_from_points(points, return_delaunay=True)

            lines = []
            for u, v in voronoi.edges():
                lines.append({
                    'start': voronoi.vertex_coordinates(u, 'xy'),
                    'end'  : voronoi.vertex_coordinates(v, 'xy')
                })

            boundary = set(delaunay.vertices_on_boundary())

            plotter = MeshPlotter(delaunay)

            plotter.draw_xlines(lines)

            plotter.draw_vertices(radius=0.075, facecolor={key: '#0092d2' for key in delaunay.vertices() if key not in boundary})
            plotter.draw_edges(color='#cccccc')

            plotter.show()

    """
    delaunay = Mesh.from_vertices_and_faces(points, mesh_delaunay_from_points(points))
    voronoi  = mesh_dual(delaunay)
    for key in voronoi.vertices():
        a, b, c = delaunay.face_coordinates(key)
        center, radius, normal = circle_from_points_xy(a, b, c)
        voronoi.vertex[key]['x'] = center[0]
        voronoi.vertex[key]['y'] = center[1]
        voronoi.vertex[key]['z'] = center[2]
    if return_delaunay:
        return voronoi, delaunay
    return voronoi


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from numpy import random
    from numpy import hstack
    from numpy import zeros

    from compas.datastructures import Mesh
    from compas.datastructures import FaceNetwork
    from compas.datastructures import network_find_faces
    from compas.datastructures import network_dual
    from compas.visualization import MeshPlotter
    from compas.visualization import NetworkPlotter
    from compas.datastructures import mesh_flip_cycles

    points = [[2853.0, -29.0, 594.0], [2922.0, -29.0, 594.0], [2922.0, 59.0, 594.0], [2853.0, 59.0, 594.0], [3028.0, -29.0, 594.0], [3097.0, -29.0, 594.0], [3097.0, 59.0, 594.0], [3028.0, 59.0, 594.0]]

    faces = mesh_delaunay_from_points(points)

    mesh = Mesh.from_vertices_and_faces(points, faces)

    key_index = mesh.key_index()
    vertices = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
    edges = [(key_index[u], key_index[v]) for u, v in mesh.edges()]

    network = FaceNetwork.from_vertices_and_edges(vertices, edges)

    network_find_faces(network, breakpoints=None)

    f0 = [fkey for fkey in network.faces() if len(network.face_vertices(fkey)) > 3][0]
    v0 = network.face_vertices(f0)

    for i in range(-1, len(v0) - 1):
        u = v0[i]
        v = v0[i + 1]
        network.halfedge[u][v] = None

    del network.face[f0]

    for i in range(-1, len(v0) - 1):
        u = v0[i]
        v = v0[i + 1]
        fkey = network._get_facekey(None)
        network.face[fkey] = [u, v]
        network.halfedge[u][v] = fkey

    for u, v in network.edges():
        print u, v, ':', network.halfedge[u][v], network.halfedge[v][u]

    dual = network_dual(network)

    plotter = NetworkPlotter(network)

    lines = []
    for u, v in dual.edges():
        lines.append({
            'start': dual.vertex_coordinates(u, 'xy'),
            'end': dual.vertex_coordinates(v, 'xy'),
            'width': 1.0,
            'color': '#cccccc'
        })

    plotter.draw_vertices(radius=2.0, text={key: key for key in network.vertices()})
    plotter.draw_faces(text={fkey: str(fkey) for fkey in network.faces()}, facecolor='#eeeeee')
    plotter.draw_xlines(lines)

    plotter.show()

    # # points = hstack((10.0 * random.random_sample((20, 2)), zeros((20, 1)))).tolist()
    # # mesh = Mesh.from_vertices_and_faces(points, mesh_delaunay_from_points(points))

    # # trimesh_optimise_topology(mesh, 1.0, allow_boundary_split=True)

    # # points = [mesh.vertex_coordinates(key) for key in mesh.vertices()]

    # voronoi, delaunay = mesh_voronoi_from_points(points, return_delaunay=True)

    # lines = []
    # for u, v in voronoi.edges():
    #     lines.append({
    #         'start': voronoi.vertex_coordinates(u, 'xy'),
    #         'end'  : voronoi.vertex_coordinates(v, 'xy'),
    #         'width': 1.0
    #     })

    # boundary = set(delaunay.vertices_on_boundary())

    # plotter = MeshPlotter(delaunay)

    # plotter.draw_vertices(radius=0.075, facecolor={key: '#0092d2' for key in delaunay.vertices() if key not in boundary})
    # plotter.draw_edges(color='#cccccc')
    # plotter.draw_xlines(lines)

    # plotter.show()

    # # delaunay.plot(
    # #     vertexsize=0.075,
    # #     faces_on=False,
    # #     edgecolor='#cccccc',
    # #     vertexcolor={key: '#0092d2' for key in delaunay if key not in boundary},
    # #     lines=lines
    # # )
