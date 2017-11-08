from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import project_points_plane
from compas.geometry import centroid_points

from compas.geometry import distance_point_point
from compas.geometry import distance_line_line
from compas.geometry import bestfit_plane

from compas.utilities import window


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'flatness',
    'planarize_faces',

    'mesh_flatness',
    'mesh_planarize_faces',
    'mesh_planarize_faces_shapeop',
    'mesh_circularize_faces_shapeop',
]


def flatness(vertices, faces, maxdev=1.0):
    """Compute mesh flatness per face.

    Parameters
    ----------
    vertices : list
        The vertex coordinates.
    faces : list
        The face vertices.
    maxdev : float, optional
        A maximum value for the allowed deviation from flatness.
        Default is ``1.0``.

    Returns
    -------
    dict
        For each face, a deviation from *flatness*.

    Note
    ----
    The "flatness" of a face is expressed as the ratio of the distance between
    the diagonals to the average edge length. For the fabrication of glass panels,
    for example, ``0.02`` could be a reasonable maximum value.

    Warning
    -------
    This function only works as expected for quadrilateral faces.

    Example
    -------
    >>>

    """
    dev = []
    for face in faces:
        points = [vertices[index] for index in face]
        lengths = [distance_point_point(a, b) for a, b in window(points + points[0:1], 2)]
        l = sum(lengths) / len(lengths)
        d = distance_line_line((points[0], points[2]), (points[1], points[3]))
        dev.append((d / l) / maxdev)
    return dev


def planarize_faces(vertices,
                    faces,
                    fixed=None,
                    kmax=100,
                    callback=None,
                    callback_args=None):
    """Planarise a set of connected faces.

    Planarisation is implemented as a two-step iterative procedure. At every
    iteration, faces are first individually projected to their best-fit plane,
    and then the vertices are projected to the centroid of the disconnected
    corners of the faces.

    Parameters
    ----------
    vertices : list
        The vertex coordinates.
    faces : list
        The vertex indices per face.
    fixed : list, optional [None]
        A list of fixed vertices.
    kmax : int, optional [100]
        The number of iterations.
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

        positions = [[] for _ in range(len(vertices))]

        for face in iter(faces):
            points = [vertices[index] for index in face]
            plane = bestfit_plane(points)
            projections = project_points_plane(points, plane)

            for i, index in enumerate(face):
                positions[index].append(projections[i])

        for index, vertex in enumerate(vertices):
            if index in fixed:
                continue

            x, y, z = centroid_points(positions[index])
            vertex[0] = x
            vertex[1] = y
            vertex[2] = z

        if callback:
            callback(k, callback_args)


# ==============================================================================
# mesh variations
# ==============================================================================


def mesh_flatness(mesh, maxdev=1.0):
    """Compute mesh flatness per face.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.
    maxdev : float, optional
        A maximum value for the allowed deviation from flatness.
        Default is ``1.0``.

    Returns
    -------
    dict
        For each face, a deviation from *flatness*.

    Note
    ----
    The "flatness" of a face is expressed as the ratio of the distance between
    the diagonals to the average edge length. For the fabrication of glass panels,
    for example, ``0.02`` could be a reasonable maximum value.

    Warning
    -------
    This function only works as expected for quadrilateral faces.

    """
    vertices = {key: mesh.vertex_coordinates(key) for key in mesh.vertices()}
    faces = [mesh.face_vertices(fkey) for fkey in mesh.faces()]
    return flatness(vertices, faces, maxdev=maxdev)


def mesh_planarize_faces(mesh, fixed=None, kmax=100, callback=None, callback_args=None):
    """Planarise a set of connected faces.

    Planarisation is implemented as a two-step iterative procedure. At every
    iteration, faces are first individually projected to their best-fit plane,
    and then the vertices are projected to the centroid of the disconnected
    corners of the faces.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.
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

    vertices = {key: mesh.vertex_coordinates(key) for key in mesh.vertices()}
    faces = [mesh.face_vertices(fkey) for fkey in mesh.faces()]

    for k in range(kmax):
        planarize_faces(vertices, faces, fixed=fixed, kmax=1)

        for key, attr in mesh.vertices(True):
            attr['x'] = vertices[key][0]
            attr['y'] = vertices[key][1]
            attr['z'] = vertices[key][2]

        if callback:
            callback(k, callback_args)


def mesh_planarize_faces_shapeop(mesh,
                                 fixed=None,
                                 kmax=100,
                                 callback=None,
                                 callback_args=None):
    """Planarize the faces of a mesh using ShapeOp.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.
    fixed : list, optional [None]
        A list of fixed vertices.
    kmax : int, optional [100]
        The number of iterations.
    callback : callable, optional [None]
        A user-defined callback that is called after every iteration.
    callback_args : list, optional [None]
        A list of arguments to be passed to the callback function.

    Note
    ----
    This planarization algorithm relies on the Python binding of the ShapeOp
    library. Installation instructions are available in :mod:`compas.interop`.

    Examples
    --------
    >>>

    """
    from compas.interop import shapeop

    if callback:
        if not callable(callback):
            raise Exception('The callback is not callable.')

    fixed = fixed or []
    fixed = set(fixed)

    # create a shapeop solver
    solver = shapeop.ShapeOpSolver()

    # make a key-index map
    # and count the number of vertices in the mesh
    key_index = mesh.key_index()

    # get the vertex coordinates
    xyz = mesh.get_vertices_attributes('xyz')

    # set the coordinates in the solver
    solver.set_points(xyz)

    # add a plane constraint to all faces
    for fkey in mesh.faces():
        vertices = [key_index[key] for key in mesh.face_vertices(fkey)]
        solver.add_plane_constraint(vertices, 1.0)

    # add a closeness constraint to the fixed vertices
    for key in fixed:
        vertex = key_index[key]
        solver.add_closeness_constraint(vertex, 1.0)

    for k in range(kmax):
        # solve
        solver.solve(1)
        # update the points array
        points = solver.get_points()
        # update
        for index, (key, attr) in enumerate(mesh.vertices(True)):
            index *= 3
            attr['x'] = points[index + 0]
            attr['y'] = points[index + 1]
            attr['z'] = points[index + 2]
        # callback
        if callback:
            callback(k, callback_args)

    # clean up
    solver.delete()


def mesh_circularize_faces_shapeop(mesh,
                                   fixed=None,
                                   kmax=100,
                                   callback=None,
                                   callback_args=None):
    """Circularize the faces of a mesh using ShapeOp.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.
    fixed : list, optional [None]
        A list of fixed vertices.
    kmax : int, optional [100]
        The number of iterations.
    callback : callable, optional [None]
        A user-defined callback that is called after every iteration.
    callback_args : list, optional [None]
        A list of arguments to be passed to the callback function.

    Note
    ----
    This cicularization algorithm relies on the Python binding of the ShapeOp
    library. Installation instructions are available in :mod:`compas.interop`.

    Examples
    --------
    >>>

    """
    from compas.interop import shapeop

    if callback:
        if not callable(callback):
            raise Exception('The callback is not callable.')

    fixed = fixed or []
    fixed = set(fixed)

    # create a shapeop solver
    solver = shapeop.ShapeOpSolver()

    # make a key-index map
    # and count the number of vertices in the mesh
    key_index = mesh.key_index()

    # get the vertex coordinates
    xyz = mesh.get_vertices_attributes('xyz')

    # set the coordinates in the solver
    solver.set_points(xyz)

    # add a plane constraint to all faces
    for fkey in mesh.faces():
        vertices = [key_index[key] for key in mesh.face_vertices(fkey)]
        solver.add_circle_constraint(vertices, 1.0)

    # add a closeness constraint to the fixed vertices
    for key in fixed:
        vertex = key_index[key]
        solver.add_closeness_constraint(vertex, 1.0)

    for k in range(kmax):
        # solve
        solver.solve(1)
        # update the points array
        points = solver.get_points()
        # update
        for index, (key, attr) in enumerate(mesh.vertices(True)):
            index *= 3
            attr['x'] = points[index + 0]
            attr['y'] = points[index + 1]
            attr['z'] = points[index + 2]
        # callback
        if callback:
            callback(k, callback_args)

    # clean up
    solver.delete()


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures import Mesh
    from compas.plotters import MeshPlotter
    from compas.utilities import i_to_rgb

    mesh = Mesh.from_obj(compas.get_data('hypar.obj'))

    for key, attr in mesh.vertices(True):
        attr['is_fixed'] = mesh.vertex_degree(key) == 2

    fixed  = [key for key in mesh.vertices_where({'is_fixed': True})]
    radius = {key: (0.05 if key in fixed else 0.01) for key in mesh.vertices()}

    plotter = MeshPlotter(mesh, figsize=(10, 7))

    plotter.draw_vertices(radius=radius)
    plotter.draw_faces()
    plotter.draw_edges()

    key_index = mesh.key_index()
    vertices = mesh.get_vertices_attributes('xyz')
    faces = [[key_index[key] for key in mesh.face_vertices(fkey)] for fkey in mesh.faces()]
    fixed = [key_index[key] for key in fixed]

    def callback(k, args):
        if k % 10 == 0:
            dev = flatness(vertices, faces, maxdev=0.02)

            for key, attr in mesh.vertices(True):
                index = key_index[key]
                attr['x'] = vertices[index][0]
                attr['y'] = vertices[index][1]
                attr['z'] = vertices[index][2]

            plotter.update_vertices(radius=radius)
            plotter.update_faces(facecolor={fkey: i_to_rgb(dev[fkey]) for fkey in mesh.faces()})
            plotter.update_edges()
            plotter.update()

    planarize_faces(vertices, faces, fixed=fixed, kmax=1000, callback=callback)

    plotter.show()
