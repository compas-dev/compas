from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import bestfit_plane_from_points
from compas.geometry import project_points_plane
from compas.geometry import centroid_points

from compas.geometry import cross_vectors
from compas.geometry import subtract_vectors
from compas.geometry import angle_smallest_vectors
from compas.geometry import dot_vectors
from compas.geometry import scale_vector

from compas.utilities import window


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'planarize_faces',
    'flatness',
]


# flatness should be measured as the ratio of the distance between the diagonals
# and the average edge length
# this should not exceed 2%
# note that this only works for quad meshes

def flatness(vertices, faces):
    """Compute mesh flatness per face.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.

    Returns
    -------
    dict
        For each face, a deviation from *flatness*.

    Note
    ----
    The "flatness" of a face is expressed as the average of the angles between
    the normal at each face corner and the normal of the best-fit plane.

    """
    dev = []
    for face in faces:
        points = [vertices[index] for index in face]
        base, normal = bestfit_plane_from_points(points)
        angles = []
        for a, b, c in window(points + points[0:2], 3):
            u = subtract_vectors(a, b)
            v = subtract_vectors(c, b)
            n = cross_vectors(u, v)
            if dot_vectors(n, normal) > 0:
                angle = angle_smallest_vectors(n, normal)
            else:
                angle = angle_smallest_vectors(n, scale_vector(normal, -1))
            angles.append(angle)
        dev.append(sum(angles) / len(angles))
    return dev


def planarize_faces(vertices,
                    faces,
                    fixed=None,
                    kmax=100,
                    d=1.0,
                    callback=None,
                    callback_args=None):
    """Planarise the faces of a mesh.

    Planarisation is implemented as a two-step iterative procedure. At every
    iteration, faces are first individually projected to their best-fit plane,
    and then the vertices are projected to the centroid of the disconnected
    corners of the faces.

    Parameters
    ----------
    vertices : dict
        The vertex coordinates.
    faces : list
        The vertex identifiers per face.
    fixed : list, optional [None]
        A list of fixed vertices.
    kmax : int, optional [100]
        The number of iterations.
    d : float, optional [1.0]
        A damping factor.
    callback : callable, optional [None]
        A user-defined callback that is called after every iteration.
    callback_args : list, optional [None]
        A list of arguments to be passed to the callback function.

    """

    if callback:
        if not callable(callback):
            raise Exception('The callback is not callable.')

    fixed = fixed or []
    fixed = set(fixed)

    for k in range(kmax):

        positions = {key: [] for key in vertices}

        for face in iter(faces):
            points = [vertices[key] for key in face]
            plane = bestfit_plane_from_points(points)
            projections = project_points_plane(points, plane)

            for index, key in enumerate(face):
                positions[key].append(projections[index])

        for key, xyz in vertices.items():
            if key in fixed:
                continue

            x, y, z = centroid_points(positions[key])
            xyz[0] = x
            xyz[1] = y
            xyz[2] = z

        if callback:
            callback(mesh, k, callback_args)


# def planarize_shapeop(mesh,
#                       fixed=None,
#                       kmax=100,
#                       d=0.1,
#                       callback=None,
#                       callback_args=None):
#     """Planarize the faces of a mesh using ShapeOp.

#     Parameters
#     ----------
#     mesh : Mesh
#         A mesh object.
#     fixed : list, optional [None]
#         A list of fixed vertices.
#     kmax : int, optional [100]
#         The number of iterations.
#     d : float, optional [0.1]
#         A damping factor.
#     callback : callable, optional [None]
#         A user-defined callback that is called after every iteration.
#     callback_args : list, optional [None]
#         A list of arguments to be passed to the callback function.

#     Note
#     ----
#     This planarization algorithm relies on the Python binding of the ShapeOp
#     library. Installation instructions are available in ``compas.interop.shapeop``.

#     Examples
#     --------
#     >>>

#     """
#     from compas.interop import shapeop

#     if callback:
#         if not callable(callback):
#             raise Exception('The callback is not callable.')

#     fixed = fixed or []
#     fixed = set(fixed)

#     shapeop.planarize_mesh(mesh, fixed=fixed, kmax=kmax)


# def mesh_circularize(mesh,
#                      fixed=None,
#                      kmax=100,
#                      d=1.0,
#                      callback=None,
#                      callback_args=None):
#     """Circularize the faces of a mesh using ShapeOp.

#     Parameters
#     ----------
#     mesh : Mesh
#         A mesh object.
#     fixed : list, optional [None]
#         A list of fixed vertices.
#     kmax : int, optional [100]
#         The number of iterations.
#     d : float, optional [1.0]
#         A damping factor.
#     callback : callable, optional [None]
#         A user-defined callback that is called after every iteration.
#     callback_args : list, optional [None]
#         A list of arguments to be passed to the callback function.

#     Note
#     ----
#     ...

#     Examples
#     --------
#     >>>

#     """

#     # map the corners of the faces to a circle on the nearest plane
#     # use circle from points
#     # map vertices to the centroids of the face corners

#     raise NotImplementedError


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures import Mesh

    from compas.visualization.viewers.viewer import Viewer

    from compas.visualization.viewers.core.drawing import draw_points
    from compas.visualization.viewers.core.drawing import draw_lines
    from compas.visualization.viewers.core.drawing import draw_circle

    mesh = Mesh.from_obj(compas.get_data('hypar.obj'))

    for key, attr in mesh.vertices(True):
        attr['is_fixed'] = mesh.vertex_degree(key) == 2

    vertices = {key: mesh.vertex_coordinates(key) for key in mesh.vertices()}
    faces = [mesh.face_vertices(fkey) for fkey in mesh.faces()]
    fixed = mesh.vertices_where({'is_fixed': True})

    planarize_faces(vertices, faces, fixed=fixed, kmax=100)

    for key, xyz in vertices.items():
        mesh.vertex[key]['x'] = xyz[0]
        mesh.vertex[key]['y'] = xyz[1]
        mesh.vertex[key]['z'] = xyz[2]

    # deviations = []

    # for fkey, attr in mesh.faces(True):
    #     points = mesh.face_coordinates(fkey)
    #     base, normal = bestfit_plane_from_points(points)

    #     angles = []
    #     for a, b, c in window(points + points[0:2], n=3):
    #         u = vector_from_points(b, a)
    #         v = vector_from_points(b, c)
    #         w = cross_vectors(v, u)
    #         angles.append(angle_smallest_vectors_degrees(normal, w))

    #     dev = sum(angles) / len(angles)
    #     deviations.append(dev)

    # print max(deviations)
    # print min(deviations)

    points = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
    lines = [(mesh.vertex_coordinates(u), mesh.vertex_coordinates(v)) for u, v in mesh.wireframe()]

    def draw_mesh():
        draw_points(points)
        draw_lines(lines)

    def draw_circles():
        draw_circle((((0, 0, 0), (1.0, 1.0, 1.0)), 1.0))

    viewer = Viewer()

    viewer.displayfuncs += [draw_mesh, draw_circles]

    viewer.setup()
    viewer.show()
